import json


def get_shipments():
    with open("data/shipments.json", "r") as file:
        return json.load(file)


def update_shipment(shipment_id, new_status, delay_days=0):
    shipments = get_shipments()

    for shipment in shipments:
        if shipment["shipment_id"] == shipment_id:
            shipment["status"] = new_status
            shipment["delay_days"] = delay_days

    with open("data/shipments.json", "w") as file:
        json.dump(shipments, file, indent=4)

    return shipments