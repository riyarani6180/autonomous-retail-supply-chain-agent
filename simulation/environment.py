import json
import os


# Load JSON data
def load_data(file_path):

    with open(file_path, "r") as file:
        return json.load(file)


# Get complete supply chain state
def get_environment_state():

    state = {
        "inventory": load_data("data/inventory.json"),
        "shipments": load_data("data/shipments.json"),
        "vendors": load_data("data/vendors.json"),
        "routes": load_data("data/routes.json")
    }

    return state


# Display current supply chain state
def show_environment():

    state = get_environment_state()

    print("\n" + "=" * 60)
    print("🏭 CURRENT SUPPLY CHAIN ENVIRONMENT")
    print("=" * 60)

    print("\n📦 INVENTORY:")
    for item in state["inventory"]:
        print(
            f"{item['product']} | "
            f"Warehouse: {item['warehouse']} | "
            f"Stock: {item['stock']}"
        )

    print("\n🚚 SHIPMENTS:")
    for shipment in state["shipments"]:
        print(
            f"{shipment['shipment_id']} | "
            f"{shipment['product']} | "
            f"Status: {shipment['status']} | "
            f"Delay: {shipment['delay_days']} days"
        )

    print("\n🏪 VENDORS:")
    for vendor in state["vendors"]:
        print(
            f"{vendor['vendor_id']} | "
            f"{vendor['name']} | "
            f"Available: {vendor['available_quantity']}"
        )

    print("\n🛣️ ROUTES:")
    for route in state["routes"]:
        print(
            f"{route['route_id']} | "
            f"{route['origin']} → {route['destination']} | "
            f"Available: {route['available']}"
        )

    print("=" * 60)

    return state


# Reset the simulation to the original state
def reset_environment():

    original_inventory = [
        {
            "product_id": "P001",
            "product": "Gaming Laptop",
            "warehouse": "Bhubaneswar",
            "stock": 8,
            "reorder_point": 10,
            "daily_demand": 5
        },
        {
            "product_id": "P002",
            "product": "Wireless Mouse",
            "warehouse": "Bhubaneswar",
            "stock": 40,
            "reorder_point": 15,
            "daily_demand": 8
        },
        {
            "product_id": "P003",
            "product": "Keyboard",
            "warehouse": "Kolkata",
            "stock": 12,
            "reorder_point": 15,
            "daily_demand": 4
        }
    ]

    original_shipments = [
        {
            "shipment_id": "S001",
            "product_id": "P001",
            "product": "Gaming Laptop",
            "quantity": 20,
            "origin": "Delhi",
            "destination": "Bhubaneswar",
            "status": "IN_TRANSIT",
            "expected_days": 2,
            "delay_days": 0,
            "route_id": "R001"
        },
        {
            "shipment_id": "S002",
            "product_id": "P002",
            "product": "Wireless Mouse",
            "quantity": 30,
            "origin": "Kolkata",
            "destination": "Bhubaneswar",
            "status": "IN_TRANSIT",
            "expected_days": 1,
            "delay_days": 0,
            "route_id": "R003"
        },
        {
            "shipment_id": "S003",
            "product_id": "P003",
            "product": "Keyboard",
            "quantity": 15,
            "origin": "Kolkata",
            "destination": "Bhubaneswar",
            "status": "IN_TRANSIT",
            "expected_days": 2,
            "delay_days": 0,
            "route_id": "R003"
        }
    ]

    original_vendors = [
        {
            "vendor_id": "V001",
            "name": "TechSource",
            "product_id": "P001",
            "price": 52000,
            "delivery_days": 3,
            "carbon": 18,
            "available_quantity": 50
        },
        {
            "vendor_id": "V002",
            "name": "ElectroMart",
            "product_id": "P001",
            "price": 54000,
            "delivery_days": 2,
            "carbon": 12,
            "available_quantity": 30
        },
        {
            "vendor_id": "V003",
            "name": "QuickTech",
            "product_id": "P001",
            "price": 56000,
            "delivery_days": 1,
            "carbon": 25,
            "available_quantity": 15
        }
    ]

    original_routes = [
        {
            "route_id": "R001",
            "origin": "Delhi",
            "destination": "Bhubaneswar",
            "cost": 5000,
            "delivery_days": 2,
            "carbon": 20,
            "available": True
        },
        {
            "route_id": "R002",
            "origin": "Delhi",
            "destination": "Bhubaneswar",
            "cost": 7000,
            "delivery_days": 1,
            "carbon": 30,
            "available": True
        },
        {
            "route_id": "R003",
            "origin": "Kolkata",
            "destination": "Bhubaneswar",
            "cost": 3500,
            "delivery_days": 1,
            "carbon": 10,
            "available": True
        }
    ]

    # Write original data back to JSON files
    with open("data/inventory.json", "w") as file:
        json.dump(original_inventory, file, indent=4)

    with open("data/shipments.json", "w") as file:
        json.dump(original_shipments, file, indent=4)

    with open("data/vendors.json", "w") as file:
        json.dump(original_vendors, file, indent=4)

    with open("data/routes.json", "w") as file:
        json.dump(original_routes, file, indent=4)

    print("\n🔄 Environment has been reset successfully!")

    return get_environment_state()


# Run this file directly for testing
if __name__ == "__main__":

    print("Starting Supply Chain Simulation...")

    show_environment()