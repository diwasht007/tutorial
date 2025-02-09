from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User



def firstLetterCapital(value):  # validator
    if not str(value).isupper():
        raise ValidationError("First letter must be capitalized.")
    return value


class Store(models.Model):
    name = models.CharField(max_length=50)
    locatiton = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)  # validators=[firstLetterCapital])
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="stores", null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    apiuser = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator, MinValueValidator])
    comments = models.CharField(max_length=200, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="Reviews", null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "the rating of " + self.product.name + ":---" + str(self.rating)
