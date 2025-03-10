from config import DB_CONFIG
import mysql.connector

# Ambil nama database dari DB_CONFIG
DB_NAME = DB_CONFIG["database"]

# Koneksi ke MySQL tanpa memilih database dulu
conn = mysql.connector.connect(
    host=DB_CONFIG["host"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"]
)
cursor = conn.cursor()

# Pastikan database sudah ada
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
print(f"Database '{DB_NAME}' siap digunakan.")

# Tutup koneksi awal
cursor.close()
conn.close()

# Koneksi ulang dengan database yang sudah dibuat
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Definisi tabel (dengan pengecekan keberadaan)
tables = {
    "areas": """
        CREATE TABLE IF NOT EXISTS areas (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            country_code VARCHAR(10),
            parent_area_id INT,
            parent_area VARCHAR(255),
            flag TEXT
        );
    """,
    "competitions": """
        CREATE TABLE IF NOT EXISTS competitions (
            id INT PRIMARY KEY,
            area_id INT,
            name VARCHAR(255) NOT NULL,
            code VARCHAR(10),
            type VARCHAR(50),
            emblem TEXT,
            plan VARCHAR(50),
            last_updated TIMESTAMP,
            FOREIGN KEY (area_id) REFERENCES areas(id)
        );
    """,
    "teams": """
        CREATE TABLE IF NOT EXISTS teams (
            id INT PRIMARY KEY,
            area_id INT,
            name VARCHAR(255) NOT NULL,
            short_name VARCHAR(50),
            tla VARCHAR(10),
            crest TEXT,
            address VARCHAR(255),
            website VARCHAR(255),
            founded INT,
            club_colors VARCHAR(100),
            venue VARCHAR(100),
            FOREIGN KEY (area_id) REFERENCES areas(id)
        );
    """,
    "matches": """
        CREATE TABLE IF NOT EXISTS matches (
            id INT PRIMARY KEY,
            competition_id INT,
            season VARCHAR(10), 
            matchday INT,
            home_team_id INT,
            away_team_id INT,
            home_score INT,
            away_score INT,
            status VARCHAR(20),
            FOREIGN KEY (competition_id) REFERENCES competitions(id),
            FOREIGN KEY (home_team_id) REFERENCES teams(id),
            FOREIGN KEY (away_team_id) REFERENCES teams(id),
            utc_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
}

# Buat tabel jika belum ada
for table_name, table_sql in tables.items():
    cursor.execute(table_sql)
    print(f"Tabel '{table_name}' siap digunakan.")

# Commit perubahan dan tutup koneksi
conn.commit()
cursor.close()
conn.close()

print("Semua tabel telah diperiksa dan siap digunakan.")
