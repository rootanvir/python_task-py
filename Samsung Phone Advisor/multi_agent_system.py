import re
import psycopg2

class MultiAgentSystem:
    def __init__(self, db_config=None):
        self.db_config = db_config or {
            "dbname": "phonesdb",
            "user": "postgres",
            "password": "1234",
            "host": "localhost",
            "port": "5432"
        }

    def agent1(self, phone_name):
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        cur.execute("""
            SELECT model_name, release_date, display, battery, camera, ram, storage, price
            FROM samsung_phones
            WHERE model_name ILIKE %s
        """, (f"%{phone_name}%",))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data if data else []

    def agent2(self, phone1_data, phone2_data):
        try:
            if not phone1_data or not phone2_data:
                return "⚠️ Could not find data for one or both phones."

            p1 = phone1_data[0]
            p2 = phone2_data[0]

            def extract_number(text):
                match = re.search(r"(\d+(?:\.\d+)?)", text.replace(",", ""))
                return float(match.group(1)) if match else 0

            def extract_ram(text):
                match = re.search(r"(\d+)\s*GB", text.upper())
                return int(match.group(1)) if match else 0

            def display_score(text):
                score = 0
                if "AMOLED" in text.upper(): score += 15
                if "LTPO" in text.upper(): score += 10
                if "120HZ" in text.upper(): score += 10
                if "HDR" in text.upper(): score += 5
                return score

            # --- Extract data ---
            p1_battery = extract_number(p1[3])
            p2_battery = extract_number(p2[3])
            p1_ram = extract_ram(p1[5])
            p2_ram = extract_ram(p2[5])
            p1_price = extract_number(p1[7])
            p2_price = extract_number(p2[7])
            p1_display = display_score(p1[2])
            p2_display = display_score(p2[2])

            # --- Performance scoring ---
            def performance_index(ram, battery, display, price):
                return (ram * 5) + (battery / 1000 * 10) + display - (price * 0.01)

            p1_perf = performance_index(p1_ram, p1_battery, p1_display, p1_price)
            p2_perf = performance_index(p2_ram, p2_battery, p2_display, p2_price)

            # --- Comparison output ---
            result = f"\n📱 Comparing {p1[0]} and {p2[0]}:\n"
            result += f"- Display: {p1[2]} vs {p2[2]}\n"
            result += f"- Battery: {p1[3]} vs {p2[3]}\n"
            result += f"- Camera: {p1[4]} vs {p2[4]}\n"
            result += f"- RAM: {p1[5]} vs {p2[5]}\n"
            result += f"- Storage: {p1[6]} vs {p2[6]}\n"
            result += f"- Price: {p1[7]} vs {p2[7]}\n\n"

            # --- Verdict ---
            result += f"⚙️ Performance Index:\n"
            result += f"  {p1[0]} → {p1_perf:.2f}\n"
            result += f"  {p2[0]} → {p2_perf:.2f}\n\n"

            if p1_perf > p2_perf:
                diff = p1_perf - p2_perf
                verdict = f"🏆 {p1[0]} clearly outperforms {p2[0]} by {diff:.1f} points. It's a better choice for power users."
            elif p2_perf > p1_perf:
                diff = p2_perf - p1_perf
                verdict = f"🏆 {p2[0]} outperforms {p1[0]} by {diff:.1f} points, offering stronger performance and efficiency."
            else:
                verdict = "⚖️ Both phones deliver nearly identical overall performance."

            # Price-to-performance tip
            if p1_price and p2_price:
                cheaper = p1[0] if p1_price < p2_price else p2[0]
                verdict += f"\n💰 However, {cheaper} offers better value for the price."

            result += verdict
            return result

        except Exception as e:
            return f"❌ Error generating review: {e}"
        
        
        
        
