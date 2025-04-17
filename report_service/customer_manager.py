from report_service.config_db import load_customer_config

from report_service.config_db import load_customer_config

def get_customer_info(customer_id):
    data = load_customer_config(customer_id)
    if data:
        return data
    return None

