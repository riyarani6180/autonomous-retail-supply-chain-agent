import json


def get_vendors():
    with open("data/vendors.json", "r") as file:
        return json.load(file)


def get_available_vendors(product_id):
    vendors = get_vendors()

    return [
        vendor
        for vendor in vendors
        if vendor["product_id"] == product_id
        and vendor["available_quantity"] > 0
    ]