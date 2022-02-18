from pyexpat import model
import uuid
from django.db import models
from django.core import validators


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(
        max_length=255, validators=[validators.validate_email]
    )


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255)
    order_date = models.DateTimeField()

    def add_item(self, product: Product, quantity: int = 1) -> None:
        try:
            item = self.items.get(product=product)
            item.quantity += quantity
            item.save()
        except OrderItem.DoesNotExist:
            self.items.create(
                product=product, quantity=quantity, price=product.price
            )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(
        validators=[validators.MinValueValidator(limit_value=1)]
    )
