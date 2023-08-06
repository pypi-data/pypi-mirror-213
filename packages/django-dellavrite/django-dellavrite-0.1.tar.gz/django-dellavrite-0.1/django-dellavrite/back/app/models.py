from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class MyUser(AbstractUser):
    fio = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('password', 'fio', 'username')


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_price = models.PositiveIntegerField(null=True)
