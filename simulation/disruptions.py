import json


# -----------------------------
# SIMULATE SHIPMENT DELAY
# -----------------------------
def simulate_shipment_delay(shipment_id, delay_days):

    with open("data/shipments.json", "r") as file:
        shipments = json.load(file)

    for shipment in shipments:

        if shipment["shipment_id"] == shipment_id:

            shipment["status"] = "DELAYED"
            shipment["delay_days"] = delay_days

    with open("data/shipments.json", "w") as file:
        json.dump(shipments, file, indent=4)

    return shipments


# -----------------------------
# SIMULATE VENDOR FAILURE
# -----------------------------
def simulate_vendor_failure(vendor_id):

    with open("data/vendors.json", "r") as file:
        vendors = json.load(file)

    for vendor in vendors:

        if vendor["vendor_id"] == vendor_id:

            vendor["available_quantity"] = 0

    with open("data/vendors.json", "w") as file:
        json.dump(vendors, file, indent=4)

    return vendors


# -----------------------------
# SIMULATE ROUTE CLOSURE
# -----------------------------
def simulate_route_closure(route_id):

    with open("data/routes.json", "r") as file:
        routes = json.load(file)

    for route in routes:

        if route["route_id"] == route_id:

            route["available"] = False

    with open("data/routes.json", "w") as file:
        json.dump(routes, file, indent=4)

    return routes


# -----------------------------
# SIMULATE STOCKOUT
# -----------------------------
def simulate_stockout(product_id):

    with open("data/inventory.json", "r") as file:
        inventory = json.load(file)

    for item in inventory:

        if item["product_id"] == product_id:

            item["stock"] = 0

    with open("data/inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

    return inventory