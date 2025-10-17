"""
RAG-style retrieval module for Samsung specs stored in Postgres.

Usage:
  advisor = RAGModule(db_config)
  print(advisor.answer("What are the specs of Galaxy S25 Ultra?"))
  print(advisor.answer("How much RAM does Galaxy A17 have?"))
  print(advisor.answer("Compare Galaxy Z Fold7 and Galaxy Z Flip7 for battery"))

Assumes table `samsung_phones` with columns:
  id, model_name, release_date, display, battery, camera, ram, storage, price
"""

import re
import psycopg2
from psycopg2.extras import RealDictCursor

# Simple mapping from natural-language attribute keywords to DB column names
ATTR_KEYWORDS = {
    "release": "release_date",
    "released": "release_date",
    "announce": "release_date",
    "announced": "release_date",
    "display": "display",
    "screen": "display",
    "battery": "battery",
    "camera": "camera",
    "main camera": "camera",
    "front camera": "camera",
    "selfie": "camera",
    "ram": "ram",
    "memory": "storage",   # confusing: 'memory' often maps to storage; handle both
    "storage": "storage",
    "price": "price",
    "cost": "price",
    "all": "ALL",          # special token: request all columns
    "specs": "ALL",
    "specifications": "ALL"
}

# Columns order for full-spec responses
ALL_COLUMNS = ["model_name", "release_date", "display", "battery", "camera", "ram", "storage", "price"]


class RAGModule:
    def __init__(self, db_config):
        """
        db_config: dict with keys dbname,user,password,host,port
        """
        self.db_config = db_config

    def _connect(self):
        return psycopg2.connect(cursor_factory=RealDictCursor, **self.db_config)

    def _find_models(self, text, top_k=3):
        """
        Try to find model(s) referenced in the text.
        Strategy:
          1. Look for tokens matching typical brand/model patterns
          2. If none, run a fuzzy search on model_name using ILIKE for each token combination
        Returns list of candidate dict rows (model_name and id)
        """
        # naive extraction: look for "Galaxy ..." patterns
        pattern = re.compile(r"(galaxy\s+[a-z0-9\-\+ ]{1,40})", re.I)
        found = pattern.findall(text)
        candidates = []

        conn = self._connect()
        cur = conn.cursor()
        try:
            # 1) direct pattern matches -> lookup exact-ish
            for f in found:
                term = f.strip()
                cur.execute("SELECT id, model_name FROM samsung_phones WHERE model_name ILIKE %s LIMIT %s", (f"%{term}%", top_k))
                rows = cur.fetchall()
                for r in rows:
                    if r not in candidates:
                        candidates.append(r)

            # 2) if none found, try tokens from text (e.g., "S25 Ultra")
            if not candidates:
                # try words with numbers/letters, common tokens
                tokens = re.findall(r"[A-Za-z0-9\+\-]{2,}", text)
                tokens = [t for t in tokens if len(t) > 1]
                # build queries from 1-3 token windows
                checked = set()
                for size in (3, 2, 1):
                    for i in range(len(tokens) - size + 1):
                        phrase = " ".join(tokens[i:i+size])
                        if phrase.lower() in checked: 
                            continue
                        checked.add(phrase.lower())
                        cur.execute("SELECT id, model_name FROM samsung_phones WHERE model_name ILIKE %s LIMIT %s", (f"%{phrase}%", top_k))
                        rows = cur.fetchall()
                        for r in rows:
                            if r not in candidates:
                                candidates.append(r)
                        if len(candidates) >= top_k:
                            break
                    if len(candidates) >= top_k:
                        break
        finally:
            cur.close()
            conn.close()

        # return at most top_k unique candidates
        return candidates[:top_k]

    def _detect_attributes(self, question):
        """
        Detect which columns user asks about.
        Return list of columns (DB names). 'ALL' means all columns.
        """
        q = question.lower()
        cols = set()
        for kw, col in ATTR_KEYWORDS.items():
            if kw in q:
                cols.add(col)
        # if nothing matched, assume they want ALL (fallback)
        if not cols:
            return ["ALL"]
        # Normalize: if 'ALL' present, return ['ALL']
        if "ALL" in cols:
            return ["ALL"]
        # Map 'memory' special case: add ram & storage
        if "storage" in cols or "ram" in cols:
            # ensure both storage and ram can be returned if ambiguous
            pass
        return list(cols)

    def _query_specs(self, model_ids, columns):
        """
        Query DB for given model ids and columns.
        model_ids: list of integer IDs
        columns: list of columns to fetch or ['ALL']
        returns list of dict rows
        """
        conn = self._connect()
        cur = conn.cursor()
        try:
            if columns == ["ALL"]:
                cols_sql = ", ".join(ALL_COLUMNS)
            else:
                cols_sql = ", ".join([c for c in columns if c in ALL_COLUMNS])
                if not cols_sql:
                    cols_sql = ", ".join(ALL_COLUMNS)

            fmt = "(" + ",".join(["%s"] * len(model_ids)) + ")"
            query = f"SELECT {cols_sql} FROM samsung_phones WHERE id IN {fmt}"
            cur.execute(query, tuple(model_ids))
            results = cur.fetchall()
            return results
        finally:
            cur.close()
            conn.close()

    def _format_single(self, row, columns):
        """
        Format a single DB row (RealDict) into a natural-language answer.
        """
        if columns == ["ALL"]:
            columns = ALL_COLUMNS[1:]  # skip model_name since we show it
        pieces = []
        for col in columns:
            if col == "model_name":
                continue
            val = row.get(col) if isinstance(row, dict) else row.get(col)
            pieces.append(f"{col.replace('_',' ').title()}: {val if val else 'N/A'}")
        return f"{row.get('model_name')}: " + "; ".join(pieces)

    def answer(self, question):
        """
        Main entry point.
        Returns a text answer for direct factual queries.
        """
        # 1. detect attributes requested
        columns = self._detect_attributes(question)
        # 2. detect model(s)
        candidates = self._find_models(question, top_k=3)

        if not candidates:
            # no model found; if the query is general (e.g., "which has best battery under $1000"),
            # we return a short instruction stating we need model or a targeted query.
            # But per instruction, do best-effort: if price-based query, return top battery phones and include prices if present.
            if "best battery" in question.lower() or "longest battery" in question.lower():
                return self._best_battery_sample(question)
            return "I couldn't identify a specific Samsung model in your question. Try including the model name (e.g., 'Galaxy S25 Ultra')."

        # prepare model ids
        model_ids = [m["id"] for m in candidates]

        # fetch data
        rows = self._query_specs(model_ids, columns)

        # format answer
        if len(rows) == 1 or len(model_ids) == 1:
            r = rows[0]
            # if user requested ALL or multiple columns, format nicely
            if columns == ["ALL"]:
                # return full specs
                return self._format_single(r, ["ALL"])
            else:
                # map requested columns to readable sentences
                out_parts = []
                for c in columns:
                    if c == "ALL":
                        continue
                    # guard: if attribute mapped to 'storage' but DB has it combined with RAM, just return storage column
                    val = r.get(c)
                    friendly = c.replace('_',' ').title()
                    out_parts.append(f"{friendly}: {val if val else 'N/A'}")
                return f"{r.get('model_name')}: " + "; ".join(out_parts)

        # multiple rows found — return a compact comparison table
        lines = []
        header = ["Model"] + ([col.replace('_',' ').title() for col in (ALL_COLUMNS[1:] if columns==['ALL'] else columns)])
        lines.append(" | ".join(header))
        lines.append("-" * (len(lines[0]) + 5))
        for r in rows:
            row_vals = [r.get("model_name")]
            for c in (ALL_COLUMNS[1:] if columns==['ALL'] else columns):
                row_vals.append(str(r.get(c) or "N/A"))
            lines.append(" | ".join(row_vals))
        return "\n".join(lines)

    def _best_battery_sample(self, question, limit=5):
        """
        Heuristic answer for 'best battery' queries (fallback when no model specified).
        Returns top phones by battery score heuristically based on presence of '5000 mAh' etc.
        This is a simple best-effort ranking (not a true battery-discharge test).
        """
        conn = self._connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT model_name, battery, price FROM samsung_phones")
            allrows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        # crude numeric extraction of mAh
        scored = []
        for r in allrows:
            batt = r.get("battery") or ""
            m = re.search(r"(\d{3,5})\s*mAh", batt)
            if m:
                score = int(m.group(1))
            else:
                # fallback score zero if cannot parse
                score = 0
            scored.append((score, r.get("model_name"), batt, r.get("price")))
        scored.sort(reverse=True)
        top = scored[:limit]
        lines = ["Top phones by battery (mAh) — extracted heuristically:"]
        for s, name, batt, price in top:
            lines.append(f"{name} — {batt or 'N/A'} — Price: {price or 'N/A'}")
        return "\n".join(lines)
