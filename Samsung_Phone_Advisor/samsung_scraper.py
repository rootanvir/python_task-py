import csv
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time



class SamsungScraper:
    def __init__(self, csv_file="Samsung_Phone_Advisor/samsung_phones.csv", db_config=None):
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

        print(f"Scraping complete! Data saved to CSV: {self.csv_file}")

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
        print("CSV data inserted into PostgreSQL table 'samsung_phones'")

    def close_driver(self):
        self.driver.quit()
        
 