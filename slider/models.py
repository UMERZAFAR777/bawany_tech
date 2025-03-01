from django.db import models

# Create your models here.

class Slider(models.Model):
    DISCOUNT_DEALS = (
        ('NEW ARRIVAL','NEW ARRIVAL'),
        ('HOT DEALS','HOT DEALS'),
    )
    img = models.ImageField(upload_to='slider_img/', unique=True, default=None)
    brand_name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=200)
    discount_deal = models.CharField(choices=DISCOUNT_DEALS, max_length=200)

    def __str__(self):
        return self.brand_name











