def detect_disruptions(inventory, shipments):
    disruptions = []

    # Check inventory
    for item in inventory:
        if item["stock"] < item["reorder_point"]:
            disruptions.append({
                "type": "LOW_INVENTORY",
                "product_id": item["product_id"],
                "message": f"{item['product']} stock is low"
            })

    # Check shipments
    for shipment in shipments:
        if shipment["delay_days"] > 0:
            disruptions.append({
                "type": "SHIPMENT_DELAY",
                "shipment_id": shipment["shipment_id"],
                "message": f"Shipment {shipment['shipment_id']} is delayed"
            })

    return disruptions