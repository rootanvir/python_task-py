import csv
import json
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from rag_module import RAGModule
from multi_agent_system import MultiAgentSystem
from response_composer import ResponseComposer
import app
import re


class SamsungScraper:
    def __init__(self, csv_file="samsung_phones.csv", db_config=None):
        self.csv_file = csv_file
        self.db_config = db_config or {
            "dbname": "phonesdb",
            "user": "postgres",
            "password": "1234",
            "host": "localhost",
            "port": "5432"
        }
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)

        
        
    def scrape_to_csv(self):
        url = "https://www.gsmarena.com/samsung-phones-9.php"  # Example page
        self.driver.get(url)
        time.sleep(2)

        phones = self.driver.find_elements(By.CSS_SELECTOR, ".makers li a")
        print(f"Found {len(phones)} phones on the page...")

        data_list = []

        for phone in phones[:30]:  # Limit to top 30 phones
            model_name = phone.text.strip()
            link = phone.get_attribute("href")

            # Go to phone detail page
            self.driver.get(link)
            time.sleep(1)

            try:
                release_date = self.driver.find_element(By.XPATH, "//td[text()='Announced']/following-sibling::td").text
            except:
                release_date = "N/A"
            try:
                display = self.driver.find_element(By.XPATH, "//td[text()='Display']/following-sibling::td").text
            except:
                display = "N/A"
            try:
                battery = self.driver.find_element(By.XPATH, "//td[text()='Battery']/following-sibling::td").text
            except:
                battery = "N/A"
            try:
                camera = self.driver.find_element(By.XPATH, "//td[text()='Main Camera']/following-sibling::td").text
            except:
                camera = "N/A"
            try:
                ram = self.driver.find_element(By.XPATH, "//td[text()='Internal']/following-sibling::td").text
            except:
                ram = "N/A"
            try:
                storage = ram  # Sometimes storage and RAM are in same field
            except:
                storage = "N/A"
            try:
                price = self.driver.find_element(By.XPATH, "//td[text()='Price']/following-sibling::td").text
            except:
                price = "N/A"

            data_list.append([model_name, release_date, display, battery, camera, ram, storage, price])
            self.driver.back()
            time.sleep(1)

        # Save to CSV
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["model_name","release_date","display","battery","camera","ram","storage","price"])
            writer.writerows(data_list)

        print(f"✅ Scraping complete! Data saved to CSV: {self.csv_file}")

    def csv_to_postgresql(self):
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()

        with open(self.csv_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)  # Skip header row

            for row in reader:
                row = [r if r else "N/A" for r in row]
                cur.execute("""
                    INSERT INTO samsung_phones
                    (model_name, release_date, display, battery, camera, ram, storage, price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, row)

        conn.commit()
        cur.close()
        conn.close()
        print("✅ CSV data inserted into PostgreSQL table 'samsung_phones'")

    def close_driver(self):
        self.driver.quit()

# ---------- Query Interface ---------- #
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
            print(f"\n📱 {result[0]} Specs:")
            print(f"Released: {result[1]}")
            print(f"Display: {result[2]}")
            print(f"Battery: {result[3]}")
            print(f"Camera: {result[4]}")
            print(f"RAM: {result[5]}")
            print(f"Storage: {result[6]}")
            print(f"Price: {result[7]}")
        else:
            print("Model not found.")

    def compare_phones(self, model1, model2):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT model_name, camera, battery, price FROM samsung_phones
            WHERE LOWER(model_name) LIKE LOWER(%s)
               OR LOWER(model_name) LIKE LOWER(%s)
        """, (f"%{model1}%", f"%{model2}%"))
        results = cur.fetchall()
        cur.close()
        conn.close()

        if len(results) == 2:
            print("\n Comparison:")
            for r in results:
                print(f"\n{r[0]}:")
                print(f"  Camera: {r[1]}")
                print(f"  Battery: {r[2]}")
                print(f"  Price: {r[3]}")
        else:
            print("Could not find both phones for comparison.")

    def best_battery_under(self, price_limit):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT model_name, battery, price FROM samsung_phones
            WHERE price != 'N/A'
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()

        # This part would normally need numeric parsing if price data was consistent
        print(f"\n⚡ Best battery phones under ${price_limit} (approx data):")
        for r in results[:5]:
            print(f"{r[0]} → Battery: {r[1]}, Price: {r[2]}")



if __name__ == "__main__": 
    # ---------- Old scraper & advisor calls (keep for reference) ----------
    # scraper = SamsungScraper()
    # scraper.scrape_to_csv()
    # scraper.csv_to_postgresql()
    # scraper.close_driver()

    # advisor = SamsungAdvisor()
    # advisor.get_specs("Galaxy M17")
    # advisor.compare_phones("Galaxy M17", "Galaxy F36")
    # advisor.best_battery_under(1000)

    # rag = RAGModule(scraper.db_config)
    # print(rag.answer("What is the price of Galaxy A17?"))
    # print(rag.answer("Compare Galaxy S25 and Galaxy S25 Ultra for battery"))

    # con = SamsungScraper()
    # rag = RAGModule(con.db_config)
    # print(rag.answer("What are the specs of Galaxy M17?"))
    

    

    # ---------- New Multi-Agent + Response Composer ----------
    # con = SamsungScraper()
    # agents = MultiAgentSystem(con.db_config)
    # composer = ResponseComposer()

    # phone1_list = agents.agent1("Galaxy M17")
    # phone2_list = agents.agent1("Galaxy S25 Edge")

    # if not phone1_list or not phone2_list:
    #     print({"answer": "⚠️ One or both phones not found in the database."})
    # else:
    #     phone1_data = phone1_list[0]
    #     phone2_data = phone2_list[0]

    #     rag_data = {
    #         "phone1": phone1_data[0],
    #         "phone2": phone2_data[0]
    #     }

    #     # agent2 returns a concise comparison string
    #     comparison_text = agents.agent2(phone1_list, phone2_list)

    #     final_answer = composer.compose_response(rag_data, phone1_data, comparison_text)
    #     print(final_answer)
    
    
    
    # Initialize scraper, agents, and composer
    scraper = SamsungScraper()
    agents = MultiAgentSystem(scraper.db_config)
    composer = ResponseComposer()

    # User query
    question_text = "Compare Samsung Galaxy M17 and Galaxy S25 Edge"

    # Extract phone names from query (simple regex)
    phone_names = re.findall(r"Galaxy\s\S+", question_text, re.IGNORECASE)
    if len(phone_names) != 2:
        print("⚠️ Could not parse two phone names from the question.")
    else:
        # Fetch phone data from DB via agent1
        phone1_list = agents.agent1(phone_names[0])
        phone2_list = agents.agent1(phone_names[1])

        if not phone1_list or not phone2_list:
            print("⚠️ One or both phones not found in the database.")
        else:
            # Take the first match (agent1 returns list of rows)
            phone1_data = phone1_list[0]
            phone2_data = phone2_list[0]

            # Build RAG-like data for composer
            rag_data = {"phone1": phone1_data[0], "phone2": phone2_data[0]}

            # Compare phones via agent2
            comparison_text = agents.agent2(phone1_list, phone2_list)

            # Compose final answer
            final_answer = composer.compose_response(rag_data, phone1_data, comparison_text)
            print("\n✅ Answer:\n")
            print(final_answer)
    