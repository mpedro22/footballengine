import requests
import mysql.connector
from config import DB_CONFIG, API_URL, API_KEY

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Ambil semua kompetisi untuk mendapatkan tim dari masing-masing liga
cursor.execute("SELECT id FROM competitions")
competitions = cursor.fetchall()

for comp in competitions:
    comp_id = comp[0]
    url = f"{API_URL}/competitions/{comp_id}/teams"
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()

    if "teams" in data:
        for team in data["teams"]:
            sql = """
                INSERT INTO teams (id, area_id, name, short_name, tla, crest, address, website, founded, club_colors, venue)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                name=VALUES(name), short_name=VALUES(short_name), tla=VALUES(tla),
                crest=VALUES(crest), address=VALUES(address), website=VALUES(website),
                founded=VALUES(founded), club_colors=VALUES(club_colors), venue=VALUES(venue)
            """
            values = (
                team["id"], team["area"]["id"], team["name"], team.get("shortName"),
                team.get("tla"), team.get("crest"), team.get("address"), team.get("website"),
                team.get("founded"), team.get("clubColors"), team.get("venue")
            )
            cursor.execute(sql, values)

        conn.commit()
        print(f"Data tim dari kompetisi {comp_id} berhasil disimpan!")

cursor.close()
conn.close()
