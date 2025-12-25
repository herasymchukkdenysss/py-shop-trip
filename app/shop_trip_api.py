from app.customer import Customer
from app.shop import Shop
from app.location import Location
from app.car import Car


class SingleTripManager:
    def __init__(
            self,
            fuel_price: float,
            customer: Customer,
            shops: list[Shop]
    ) -> None:
        self._fuel_price = fuel_price
        self._customer = customer
        self._shops = shops
        self._expenses_map = self._get_expenses_map()

        if self._expenses_map:
            self._best_shop = min(
                self._expenses_map, key=lambda s: self._expenses_map[s]
            )
            self._min_cost = self._expenses_map[self._best_shop]
        else:
            self._best_shop = None
            self._min_cost = 0

    def _get_expenses_map(self) -> dict[Shop, float]:
        return {
            shop:
                round(self._customer.get_fuel_cost(
                    shop.location,
                    self._fuel_price
                ) * 2 + shop.calculate_cost(self._customer.product_cart), 2)
            for shop in self._shops
        }

    def print_trip(self) -> None:
        self._print_customer_balance()
        self._print_expenses()
        self._print_ride()

        if self._min_cost <= self._customer.balance:
            print()
            self._print_receipt()
            self._print_ride_home()
            self._print_customer_balance(now=True)

    def _print_customer_balance(self, now: bool = False) -> None:
        print(f"{self._customer.name}{' now ' if now else ' '}"
              f"has {round(self._customer.balance, 2)} dollars")

    def _print_expenses(self) -> None:
        for shop, cost in self._expenses_map.items():
            print(f"{self._customer.name}'s trip "
                  f"to the {shop.name} costs {cost}")

    def _print_ride(self) -> None:
        if self._min_cost > self._customer.balance:
            print(f"{self._customer.name} doesn't have "
                  f"enough money to make a purchase in any shop")
        else:
            self._customer.refuel(self._best_shop.location, self._fuel_price)
            print(f"{self._customer.name} rides to {self._best_shop.name}")

    def _print_receipt(self) -> None:
        try:
            receipt = self._best_shop.get_receipt(self._customer)
        except ValueError as e:
            print(e)
        else:
            print(receipt)

    def _print_ride_home(self) -> None:
        print(f"{self._customer.name} rides home")
        self._customer.refuel(self._best_shop.location, self._fuel_price)


class ShoppingTripApi:
    def __init__(
            self,
            data: dict
    ) -> None:
        self._fuel_price, self._customers, self._shops = self._parse_data(data)

    @classmethod
    def _parse_data(
            cls,
            data: dict
    ) -> tuple[float, list[Customer], list[Shop]]:
        fuel_price = data.get("FUEL_PRICE", 0)

        customers = []
        for customer_data in data.get("customers", []):
            car_data = customer_data["car"]
            new_customer = Customer(
                _name=customer_data["name"],
                _product_cart=customer_data["product_cart"],
                _location=Location(*customer_data["location"]),
                _money=customer_data["money"],
                _car=Car(car_data["brand"], car_data["fuel_consumption"])
            )
            customers.append(new_customer)

        shops = []
        for shop_data in data.get("shops", []):
            new_shop = Shop(
                _name=shop_data["name"],
                _location=Location(*shop_data["location"]),
                _products=shop_data["products"],
            )
            shops.append(new_shop)

        return fuel_price, customers, shops

    def print_shop_trips(self) -> None:
        total_customers = len(self._customers)

        for index, customer in enumerate(self._customers):
            trip = SingleTripManager(
                self._fuel_price,
                customer,
                self._shops
            )
            trip.print_trip()

            if index < total_customers - 1:
                print()
