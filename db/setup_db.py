import sqlite3

conn = sqlite3.connect("db/klardata.db")
cursor = conn.cursor()

# Opret kundetabel
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    report_config TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database og 'customers'-tabel oprettet.")
