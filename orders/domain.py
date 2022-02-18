from datetime import datetime
from django.utils import timezone
from django.db import transaction
from . import models


class CreateOrder:
    """
    CreateOrder use-case. Creates and order and persists it as a unit of work.
    """

    def __init__(self, customer: models.Customer) -> None:
        self._customer: models.Customer = customer

    def run(self) -> None:
        self.order = models.Order(
            order_number=self._generator_order_number(),
            order_date=self._generate_timestamp(),
            customer=self._customer,
        )
        self.order.save()
        return self.order

    def _generator_order_number(self) -> str:
        return "XXX"

    def _generate_timestamp(self) -> datetime:
        return timezone.now()


class AddItemToOrder:
    def __init__(self, order: models.Order, product: models.Product) -> None:
        self._order = order
        self._product = product

    def run(self) -> None:
        self._order.add_item(quantity=1, product=self._product)
