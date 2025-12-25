from dataclasses import dataclass

from app.location import Location
from app.car import Car


@dataclass
class Customer:

    _name: str
    _product_cart: dict
    _location: Location
    _money: float
    _car: Car

    @property
    def name(self) -> str:
        return self._name

    @property
    def balance(self) -> float:
        return self._money

    @property
    def location(self) -> Location:
        return self._location

    @property
    def product_cart(self) -> dict:
        return self._product_cart

    def get_fuel_cost(self, location: Location, fuel_price: float) -> float:
        distance = self._location.get_distance_to_location(location)
        fuel_cost = self._car.get_fuel_cost(distance, fuel_price)
        return fuel_cost

    def pay(self, amount: float) -> bool:
        if amount <= self._money:
            self._money -= amount
            return True
        return False

    def refuel(self, location: Location, fuel_price: float) -> None:
        self.pay(self.get_fuel_cost(location, fuel_price))
