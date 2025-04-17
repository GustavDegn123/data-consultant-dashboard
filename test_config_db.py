from report_service.config_db import save_customer_config, load_customer_config

customer_id = "demo001"
config = {
    "name": "Gustav Degn",
    "email": "gustavdegn@hotmail.dk",
    "report_config": {
        "sections": ["key_metrics", "insights", "time_analysis", "product_analysis"]
    }
}

save_customer_config(customer_id, config)

loaded = load_customer_config(customer_id)
print(f"\n✅ Konfiguration hentet for '{customer_id}': {loaded}")
