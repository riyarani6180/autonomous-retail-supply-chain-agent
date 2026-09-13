import json


def get_inventory():
    with open("data/inventory.json", "r") as file:
        return json.load(file)


def update_inventory(product_id, quantity):
    inventory = get_inventory()

    for item in inventory:
        if item["product_id"] == product_id:
            item["stock"] += quantity

    with open("data/inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

    return inventory