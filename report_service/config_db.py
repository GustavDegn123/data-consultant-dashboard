import sqlite3
import json

DB_PATH = "db/klardata.db"

def save_customer_config(customer_id, config_dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    name = config_dict.get("name", "Demo Kunde")
    email = config_dict.get("email", "gustavdegn@hotmail.dk")
    config_json = json.dumps(config_dict.get("report_config", {}))

    cursor.execute("""
        INSERT INTO customers (id, name, email, report_config)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            email=excluded.email,
            report_config=excluded.report_config
    """, (customer_id, name, email, config_json))

    conn.commit()
    conn.close()
    print(f"[DB] Gemte config for {customer_id}")

def load_customer_config(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, email, report_config FROM customers WHERE id = ?", (customer_id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        name, email, config_json = row
        return {
            "name": name,
            "email": email,
            "report_config": json.loads(config_json)
        }
    return None
