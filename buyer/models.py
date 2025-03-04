from django.db import models

from django.contrib.auth.models import User
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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





class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.buyer.first_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product_name} - {self.quantity}"
    


    