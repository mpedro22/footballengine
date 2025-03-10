import requests
import mysql.connector
from config import DB_CONFIG, API_URL, API_KEY

# Koneksi ke database
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Fetch data dari API
url = f"{API_URL}/areas"
headers = {"X-Auth-Token": API_KEY}
response = requests.get(url, headers=headers)
data = response.json()

# Insert data ke database
if "areas" in data:
    for area in data["areas"]:
        sql = """
            INSERT INTO areas (id, name, country_code, parent_area_id, parent_area, flag)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            name=VALUES(name), country_code=VALUES(country_code),
            parent_area_id=VALUES(parent_area_id), parent_area=VALUES(parent_area),
            flag=VALUES(flag)
        """
        values = (
            area["id"], area["name"], area.get("countryCode"),
            area.get("parentAreaId"), area["parentArea"], area.get("flag")
        )
        cursor.execute(sql, values)

    conn.commit()
    print("Data areas berhasil disimpan ke database!")

# Tutup koneksi
cursor.close()
conn.close()
