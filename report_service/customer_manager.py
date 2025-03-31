CUSTOMERS = {
    "pilot001": {
        "name": "Gustav Degn",
        "email": "gustavdegn@hotmail.dk"
    },
    # Tilføj flere kunder her
}

def get_customer_info(customer_id):
    return CUSTOMERS.get(customer_id)
