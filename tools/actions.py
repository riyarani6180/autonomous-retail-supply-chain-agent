import json


def execute_purchase(product_id, quantity, vendor_id):

    with open("data/inventory.json", "r") as file:
        inventory = json.load(file)

    with open("data/vendors.json", "r") as file:
        vendors = json.load(file)

    vendor_found = False

    for vendor in vendors:

        if vendor["vendor_id"] == vendor_id:

            if vendor["available_quantity"] < quantity:
                return {
                    "action": "PURCHASE",
                    "status": "FAILED",
                    "message": "Vendor does not have enough stock."
                }

            vendor["available_quantity"] -= quantity
            vendor_found = True
            break

    if not vendor_found:
        return {
            "action": "PURCHASE",
            "status": "FAILED",
            "message": "Vendor not found."
        }

    for item in inventory:

        if item["product_id"] == product_id:
            item["stock"] += quantity
            break

    with open("data/inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

    with open("data/vendors.json", "w") as file:
        json.dump(vendors, file, indent=4)

    return {
        "action": "PURCHASE",
        "status": "SUCCESS",
        "product_id": product_id,
        "quantity": quantity,
        "vendor_id": vendor_id
    }


def execute_reroute(shipment_id, route_id):

    with open("data/shipments.json", "r") as file:
        shipments = json.load(file)

    with open("data/routes.json", "r") as file:
        routes = json.load(file)

    route_found = False

    for route in routes:

        if route["route_id"] == route_id:

            if not route["available"]:
                return {
                    "action": "REROUTE",
                    "status": "FAILED",
                    "message": "Selected route is unavailable."
                }

            route_found = True
            break

    if not route_found:
        return {
            "action": "REROUTE",
            "status": "FAILED",
            "message": "Route not found."
        }

    shipment_found = False

    for shipment in shipments:

        if shipment["shipment_id"] == shipment_id:

            shipment["status"] = "REROUTED"
            shipment["delay_days"] = 0
            shipment["route_id"] = route_id

            shipment_found = True
            break

    if not shipment_found:
        return {
            "action": "REROUTE",
            "status": "FAILED",
            "message": "Shipment not found."
        }

    with open("data/shipments.json", "w") as file:
        json.dump(shipments, file, indent=4)

    return {
        "action": "REROUTE",
        "status": "SUCCESS",
        "shipment_id": shipment_id,
        "route_id": route_id
    }