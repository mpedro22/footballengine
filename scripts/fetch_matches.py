import requests
import mysql.connector
from config import DB_CONFIG, API_URL, API_KEY

# Koneksi ke database
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Ambil daftar kompetisi untuk mendapatkan match dari tiap liga
cursor.execute("SELECT id FROM competitions")
competitions = cursor.fetchall()

for comp in competitions:
    comp_id = comp[0]
    url = f"{API_URL}/competitions/{comp_id}/matches"
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()

    if "matches" in data:
        for match in data["matches"]:
            sql = """
                INSERT INTO matches (id, competition_id, season, matchday, home_team_id, away_team_id, 
                                     home_score, away_score, status, utc_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                home_score=VALUES(home_score), away_score=VALUES(away_score),
                status=VALUES(status), utc_date=VALUES(utc_date)
            """
            values = (
                match["id"], comp_id, match["season"]["startDate"], match["matchday"],
                match["homeTeam"]["id"], match["awayTeam"]["id"], 
                match["score"]["fullTime"]["home"], match["score"]["fullTime"]["away"], 
                match["status"], match["utcDate"]
            )
            cursor.execute(sql, values)

        conn.commit()
        print(f"Data pertandingan dari kompetisi {comp_id} berhasil disimpan!")

# Tutup koneksi
cursor.close()
conn.close()
