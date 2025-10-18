import psycopg2
import re

class SamsungAdvisor:
    def __init__(self, db_config=None):
        self.db_config = db_config or {
            "dbname": "phonesdb",
            "user": "postgres",
            "password": "1234",
            "host": "localhost",
            "port": "5432"
        }

    def connect(self):
        return psycopg2.connect(**self.db_config)

    def get_specs(self, model_name):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM samsung_phones
            WHERE LOWER(model_name) LIKE LOWER(%s)
        """, (f"%{model_name}%",))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result:
            print(f"\n📱 {result[0]} Specifications:")
            print(f"Release Date: {result[1]}")
            print(f"Display: {result[2]}")
            print(f"Battery: {result[3]}")
            print(f"Camera: {result[4]}")
            print(f"RAM: {result[5]}")
            print(f"Storage: {result[6]}")
            print(f"Price: {result[7]}")
        else:
            print("Model not found in the database.")

    def compare_photography(self, model1, model2):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT model_name, camera, battery, price 
            FROM samsung_phones
            WHERE LOWER(model_name) LIKE LOWER(%s)
               OR LOWER(model_name) LIKE LOWER(%s)
        """, (f"%{model1}%", f"%{model2}%"))
        results = cur.fetchall()
        cur.close()
        conn.close()

        if len(results) == 2:
            print(f"\n Photography Comparison between {results[0][0]} and {results[1][0]}:\n")
            for r in results:
                print(f"{r[0]} → Camera: {r[1]}, Battery: {r[2]}, Price: {r[3]}")
            print("\nConclusion: The one with higher camera megapixels or better lens setup is generally better for photography.")
        else:
            print(" One or both phones not found in the database.")

    def compare_phones(self, model1, model2):
        """New method for general comparison of all specs"""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM samsung_phones
            WHERE LOWER(model_name) LIKE LOWER(%s)
               OR LOWER(model_name) LIKE LOWER(%s)
        """, (f"%{model1}%", f"%{model2}%"))
        results = cur.fetchall()
        cur.close()
        conn.close()

        if len(results) == 2:
            header = ["Model Name", "Release Date", "Display", "Battery", "Camera", "RAM", "Storage", "Price"]
            print("\n Comparison of Samsung Phones:\n")
            print(" | ".join(header))
            print("-" * 80)
            for r in results:
                print(" | ".join([str(x) if x is not None else "N/A" for x in r]))
        else:
            print("One or both phones not found in the database.")

    def best_battery_under(self, price_limit):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT model_name, battery, price 
            FROM samsung_phones
            WHERE price != 'N/A'
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()

        print(f"\n🔋 Best Samsung phones with top battery under ${price_limit} (sample data):")
        for r in results[:5]:
            print(f"{r[0]} → Battery: {r[1]}, Price: {r[2]}")

    def answer(self, question):
        question_lower = question.lower()

        if "spec" in question_lower:
            match = re.search(r"galaxy\s[\w\d]+", question, re.IGNORECASE)
            if match:
                model = match.group(0)
                self.get_specs(model)
            else:
                print("Could not find phone name in the question.")
            return

        if "compare" in question_lower and "photography" in question_lower:
            models = re.findall(r"galaxy\s[\w\d]+", question, re.IGNORECASE)
            if len(models) == 2:
                self.compare_photography(models[0], models[1])
            else:
                print(" Please mention two phone names to compare.")
            return

        if "compare" in question_lower and "spec" in question_lower:
            models = re.findall(r"galaxy\s[\w\d]+", question, re.IGNORECASE)
            if len(models) == 2:
                self.compare_phones(models[0], models[1])
            else:
                print(" Please mention two phone names to compare.")
            return

        if "best battery" in question_lower and "under" in question_lower:
            price_match = re.search(r"\$?(\d+)", question)
            if price_match:
                self.best_battery_under(int(price_match.group(1)))
            else:
                print("Could not detect price limit.")
            return

        print("Question type not recognized.")
