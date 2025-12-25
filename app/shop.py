from dataclasses import dataclass
import datetime

from app.location import Location
from app.customer import Customer


@dataclass
class Shop:

    _name: str
    _location: Location
    _products: dict

    @property
    def name(self) -> str:
        return self._name

    @property
    def location(self) -> Location:
        return self._location

    def calculate_cost(self, product_cart: dict) -> float:
        return sum(
            self._products.get(product, 0) * quantity
            for product, quantity in product_cart.items()
        )

    def sell(self, customer: Customer) -> bool:
        cost = self.calculate_cost(customer.product_cart)
        if cost > customer.balance:
            return False
        return customer.pay(cost)

    def get_receipt(self, customer: Customer) -> str:
        if not self.sell(customer):
            return ""
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        purchases = [
            (f"{quantity} {product}{'s' if quantity > 1 else ''} for "
             f"{quantity * self._products[product]:g} dollars")
            for product, quantity in customer.product_cart.items()
        ]
        return f"""Date: {now}
Thanks, {customer.name}, for your purchase!
You have bought:
{'\n'.join(purchases)}
Total cost is {self.calculate_cost(customer.product_cart)} dollars
See you again!
"""

    def __hash__(self) -> int:
        return hash(self._name)
