import json


def get_routes():
    with open("data/routes.json", "r") as file:
        return json.load(file)


def get_available_routes():
    routes = get_routes()

    return [
        route
        for route in routes
        if route["available"]
    ]