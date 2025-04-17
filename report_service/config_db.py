# report_service/config_db.py

"""
Placeholder til fremtidig databasehåndtering af kundekonfigurationer.
"""

def save_customer_config(customer_id, config_dict):
    # TODO: Gem konfiguration i database
    print(f"[Mock] Gemmer config for {customer_id}: {config_dict}")

def load_customer_config(customer_id):
    # TODO: Hent konfiguration fra database
    print(f"[Mock] Henter config for {customer_id}")
    return {
        "sections": ["key_metrics", "insights", "product_analysis"]
    }
