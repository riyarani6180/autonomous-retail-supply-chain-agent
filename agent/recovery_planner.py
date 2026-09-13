from tools.vendors import get_available_vendors
from tools.routes import get_available_routes

from tools.optimizer import rank_options


def create_purchase_options(product_id):

    vendors = get_available_vendors(product_id)

    if not vendors:
        return []

    options = []

    for vendor in vendors:

        options.append({

            "action": "PURCHASE",

            "vendor_id": vendor["vendor_id"],

            "vendor_name": vendor["name"],

            "cost": vendor["price"],

            "delivery_days": vendor["delivery_days"],

            "carbon": vendor["carbon"],

            "available_quantity": vendor["available_quantity"]

        })

    return rank_options(options)


def create_route_options():

    routes = get_available_routes()

    if not routes:
        return []

    options = []

    for route in routes:

        options.append({

            "action": "REROUTE",

            "route_id": route["route_id"],

            "cost": route["cost"],

            "delivery_days": route["delivery_days"],

            "carbon": route["carbon"],

            "available": route["available"]

        })

    return rank_options(options)