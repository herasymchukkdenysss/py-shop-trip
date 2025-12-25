import json

from app.shop_trip_api import ShoppingTripApi


def shop_trip() -> None:
    with open("app/config.json" , "r") as json_file:
        data = json.load(json_file)

    api = ShoppingTripApi(data)

    api.print_shop_trips()
