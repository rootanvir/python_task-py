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
    "memory": "storage",
    "storage": "storage",
    "price": "price",
    "cost": "price",
    "all": "ALL",
    "specs": "ALL",
    "specifications": "ALL"
}

ALL_COLUMNS = ["id", "model_name", "release_date", "display", "battery", "camera", "ram", "storage", "price"]

class RAGModule:
    def __init__(self, db_config=None, rag_instance=None):
        self.db_config = db_config
        self.rag = rag_instance

    def _connect(self):
        return psycopg2.connect(cursor_factory=RealDictCursor, **self.db_config)

    def _detect_attributes(self, question):
        q = question.lower()
        cols = set()
        for kw, col in ATTR_KEYWORDS.items():
            if kw in q:
                cols.add(col)
        if not cols:
            return ["ALL"]
        if "ALL" in cols:
            return ["ALL"]
        return list(cols)

    def _query_specs(self, model_ids, columns):
        conn = self._connect()
        cur = conn.cursor()
        try:
            # Always include model_name for context
            if columns == ["ALL"]:
                cols_sql = ", ".join(ALL_COLUMNS)
            else:
                unique_cols = set(columns)
                unique_cols.add("model_name")
                cols_sql = ", ".join([c for c in ALL_COLUMNS if c in unique_cols])

            fmt = "(" + ",".join(["%s"] * len(model_ids)) + ")"
            query = f"SELECT {cols_sql} FROM samsung_phones WHERE id IN {fmt}"
            cur.execute(query, tuple(model_ids))
            results = cur.fetchall()

            # psycopg2 with RealDictCursor already gives dict rows
            return results
        finally:
            cur.close()
            conn.close()


    def _format_single(self, row, columns):
        if columns == ["ALL"]:
            columns = ALL_COLUMNS[2:]  # skip 'id' and 'model_name'
        pieces = []
        for col in columns:
            val = row.get(col)
            pieces.append(f"{col.replace('_',' ').title()}: {val if val else 'N/A'}")
        return f"{row.get('model_name')}: " + "; ".join(pieces)


    def answer(self, question):
        columns = self._detect_attributes(question)
        candidates = self._find_models(question, top_k=3)
    
        if not candidates:
            if "best battery" in question.lower() or "longest battery" in question.lower():
                return self._best_battery_sample(question)
            return "I couldn't identify a specific Samsung model in your question. Please include the model name."
    
        model_ids = [m["id"] for m in candidates]
        rows = self._query_specs(model_ids, columns)
    
        if not rows or len(rows) == 0:
            return "No data found for the requested models."
    
        # If only one model found
        if len(rows) == 1:
            row = rows[0]
            model = row.get("model_name", "Unknown Model")
            details = ", ".join(f"{col.title()}: {row.get(col, 'N/A')}" for col in columns if col != "model_name")
            return f"{model}: {details}"
    
        # Multi-model comparison table
        lines = []
        header = ["Model"] + ([col.replace('_',' ').title() for col in (ALL_COLUMNS[2:] if columns == ['ALL'] else columns)])
        lines.append(" | ".join(header))
        lines.append("-" * len(lines[0]))
        print("DEBUG rows:", rows)
        for r in rows:
            model_name = r.get("model_name") or "Unknown Model"
            row_vals = [model_name]
            for c in (ALL_COLUMNS[2:] if columns == ['ALL'] else columns):
                val = r.get(c, "N/A")
                row_vals.append(str(val))
            lines.append(" | ".join(row_vals))
    
        return "\n".join(lines)


    
    
    
    

    def _best_battery_sample(self, question, limit=5):
        conn = self._connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT model_name, battery, price FROM samsung_phones")
            allrows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        scored = []
        for r in allrows:
            batt = r.get("battery") or ""
            m = re.search(r"(\d{3,5})\s*mAh", batt)
            score = int(m.group(1)) if m else 0
            scored.append((score, r.get("model_name"), batt, r.get("price")))
        scored.sort(reverse=True)
        top = scored[:limit]

        lines = ["Top phones by battery (mAh) — extracted heuristically:"]
        for s, name, batt, price in top:
            lines.append(f"{name} — {batt or 'N/A'} — Price: {price or 'N/A'}")
        return "\n".join(lines)

    def _find_models(self, text, top_k=3):
        pattern = re.compile(r"Galaxy\s[\w\d]+", re.I)
        found = pattern.findall(text)
        candidates = []

        if not found:
            print("No model names detected in text:", text)
            return []

        conn = self._connect()
        cur = conn.cursor()
        try:
            for f in found:
                term = f.strip()
                cur.execute(
                    "SELECT id, model_name FROM samsung_phones WHERE model_name ILIKE %s LIMIT %s",
                    (f"%{term}%", top_k)
                )
                rows = cur.fetchall()
                for r in rows:
                    if r not in candidates:
                        candidates.append(r)
        finally:
            cur.close()
            conn.close()

        if not candidates:
            print("⚠️ No matching models found for:", text)
        return candidates[:top_k]
