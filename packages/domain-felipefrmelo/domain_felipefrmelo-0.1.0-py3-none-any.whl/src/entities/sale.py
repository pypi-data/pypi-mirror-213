from dataclasses import dataclass

from src.entities.customer import Customer
from src.entities.employee import Employee
from src.entities.product import Product

from datetime import datetime


@dataclass
class Sale:
    id: int
    customer: Customer
    employee: Employee
    products: list[Product]
    date: datetime = datetime.now()

    @property
    def total(self) -> float:
        return sum([p.price * p.quantity for p in self.products])

    @property
    def quantity(self) -> int:
        return sum([product.quantity for product in self.products])
