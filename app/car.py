from dataclasses import dataclass


@dataclass
class Car:

    _brand: str
    _fuel_consumption_100_km: float

    def get_fuel_cost(
            self,
            distance_in_km: float,
            fuel_price: float
    ) -> float:
        consumed_fuel = (self._fuel_consumption_100_km * distance_in_km) / 100
        return consumed_fuel * fuel_price
