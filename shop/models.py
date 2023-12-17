
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    CATEGORIES = [
        ('Milk', 'Milk'),
        ('Diaper', 'Diaper'),
        ('Food & Weaning food', 'Food & Weaning food'),
        ('Bath & Body care', 'Bath & Body care'),
        ('Baby accessory', 'Baby accessory'),
        ('Toy', 'Toy'),
        ('Bedroom', 'Bedroom'),
        ('Clothes', 'Clothes'),
        ('Towel', 'Towel'),
        ('Orther', 'Orther'),
    ]
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    img_path = models.CharField(max_length=40, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    featured = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.SmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.customer.user.username + "'s cart"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # cart_item = models.ManyToManyField(CartItem)
    is_deliver = models.BooleanField(default=False)
    address = models.CharField(max_length=1000)
    name_to_deliver = models.CharField(max_length=100)
    phone_to_deliver = models.CharField(max_length=11)
    note = models.CharField(max_length=1000, null=True, blank=True)
    total = models.IntegerField()

    def __str__(self) -> str:
        return str(self.customer.user.username) + "'s order"
    
    # def delete(self, *args, **kwargs):
    #     for item in self.cart_item.all():
    #         item.delete()
    #     return super().delete(*args, **kwargs)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)
    total = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.product.name + ' (' + str(self.quantity) + ')'
    
    def save(self, *args, **kwargs):
        print('saving')
        self.total = self.product.price * self.quantity
        super().save(*args, **kwargs)