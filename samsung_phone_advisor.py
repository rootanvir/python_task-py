import requests
from bs4 import BeautifulSoup
import psycopg2
import csv
import time

# === Database Connection ===
conn = psycopg2.connect(
    dbname="phonesdb",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

base_url = "https://www.gsmarena.com/"
brand_url = "https://www.gsmarena.com/samsung-phones-9.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/119.0.0.0 Safari/537.36"
}

csv_file = "samsung_phones.csv"
csv_headers = ['model_name', 'release_date', 'display', 'battery', 'camera', 'ram', 'storage', 'price']
data_rows = []

page_num = 1

while True:
    print(f"\n🔎 Scraping page {page_num} ...")
    url = f"https://www.gsmarena.com/samsung-phones-f-9-0-p{page_num}.php" if page_num > 1 else brand_url
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    phone_items = soup.select(".makers ul li a")
    if not phone_items:
        print("❌ No more phones found.")
        break

    for item in phone_items:
        model_name = item.text.strip()
        phone_link = base_url + item["href"]
        print(f"→ {model_name}")

        r2 = requests.get(phone_link, headers=headers)
        phone_soup = BeautifulSoup(r2.text, "html.parser")

        release_date = display = battery = camera = ram = storage = price = "N/A"

        for table in phone_soup.select("#specs-list table"):
            for row in table.select("tr"):
                title = row.find("td", {"class": "ttl"})
                info = row.find("td", {"class": "nfo"})
                if not title or not info:
                    continue

                t = title.text.strip().lower()
                i = info.text.strip()

                if "announced" in t:
                    release_date = i
                elif "display" in t:
                    display = i
                elif "battery" in t:
                    battery = i
                elif "camera" in t and camera == "N/A":
                    camera = i
                elif "internal" in t:
                    storage = i
                elif "ram" in i:
                    ram = i
                elif "price" in t:
                    price = i

        phone_data = [model_name, release_date, display, battery, camera, ram, storage, price]
        data_rows.append(phone_data)

        # === Insert into PostgreSQL ===
        cur.execute("""
            INSERT INTO samsung_phones (model_name, release_date, display, battery, camera, ram, storage, price)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, phone_data)
        conn.commit()

        time.sleep(1)  # be polite

    page_num += 1
    time.sleep(2)

# === Save to CSV ===
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)
    writer.writerows(data_rows)

cur.close()
conn.close()

print("\n✅ Scraping complete! Data saved to CSV and inserted into PostgreSQL.")
