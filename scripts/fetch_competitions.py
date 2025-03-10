import requests
import mysql.connector
from config import DB_CONFIG, API_URL, API_KEY

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

url = f"{API_URL}/competitions"
headers = {"X-Auth-Token": API_KEY}
response = requests.get(url, headers=headers)
data = response.json()

if "competitions" in data:
    for comp in data["competitions"]:
        sql = """
            INSERT INTO competitions (id, area_id, name, code, type, emblem, plan, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            name=VALUES(name), code=VALUES(code), type=VALUES(type),
            emblem=VALUES(emblem), plan=VALUES(plan), last_updated=VALUES(last_updated)
        """
        values = (
            comp["id"], comp["area"]["id"], comp["name"], comp.get("code"),
            comp["type"], comp.get("emblem"), comp.get("plan"), comp.get("lastUpdated")
        )
        cursor.execute(sql, values)

    conn.commit()
    print("Data kompetisi berhasil disimpan ke database!")

cursor.close()
conn.close()
