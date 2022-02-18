from django.utils import timezone
from faker import Faker
from orders import models

fake = Faker()
customer1 = models.Customer.objects.create(
    first_name=fake.first_name(),
    last_name=fake.last_name(),
    email=fake.email(),
)
customer2 = models.Customer.objects.create(
    first_name=fake.first_name(),
    last_name=fake.last_name(),
    email=fake.email(),
)

product1 = models.Product.objects.create(
    title="Product 1",
    price=34.99,
)
product2 = models.Product.objects.create(title="Product 2", price=19.99)

order1 = models.Order(
    customer=customer1,
    order_number="XXXX00001",
    order_date=timezone.now(),
)
order1.save()
order1.add_item(product=product1, quantity=2)
order1.add_item(product=product2, quantity=1)
