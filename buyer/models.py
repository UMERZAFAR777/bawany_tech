from django.db import models


class Buyer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    total_products = models.IntegerField(default=0)
    product_names = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
