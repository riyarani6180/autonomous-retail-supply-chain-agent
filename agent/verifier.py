def verify_inventory(inventory, product_id):

    for item in inventory:

        if item["product_id"] == product_id:

            if item["stock"] >= item["reorder_point"]:
                return {
                    "status": "SUCCESS",
                    "message": "Inventory level recovered",
                    "stock": item["stock"]
                }

            else:
                return {
                    "status": "FAILED",
                    "message": "Inventory is still below reorder point",
                    "stock": item["stock"]
                }

    return {
        "status": "FAILED",
        "message": "Product not found"
    }


def verify_shipment(shipments, shipment_id):

    for shipment in shipments:

        if shipment["shipment_id"] == shipment_id:

            if (
                shipment["status"] == "REROUTED"
                and shipment["delay_days"] == 0
            ):

                return {
                    "status": "SUCCESS",
                    "message": "Shipment recovered"
                }

            else:

                return {
                    "status": "FAILED",
                    "message": "Shipment still has a problem"
                }

    return {
        "status": "FAILED",
        "message": "Shipment not found"
    }