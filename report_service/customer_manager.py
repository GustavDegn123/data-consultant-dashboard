CUSTOMERS = {
    "pilot001": {
        "name": "Gustav Degn",
        "email": "gustavdegn@hotmail.dk",
        "report_config": {
            "sections": [
                "key_metrics",
                "insights",
                "time_analysis",
                "product_analysis",
                "geo_analysis"
            ]
        }
    },
    "test_customer": {
        "name": "Testkunde A/S",
        "email": "gustavdegn@hotmail.dk",
        "report_config": {
            "sections": [
                "key_metrics",
                "product_analysis"
            ]
        }
    }
}


def get_customer_info(customer_id):
    return CUSTOMERS.get(customer_id)