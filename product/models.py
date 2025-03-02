from django.db import models
from app.models import *
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    STOCK = (
        ('In Stock', 'In Stock'),
        ('Not Available', 'Not Available'),
    )
    product_name = models.CharField(max_length=200)
    img = models.CharField(max_length=200)
    discount = models.IntegerField(null=True, blank=True)  
    availability = models.CharField(choices=STOCK, max_length=100)
    link = models.CharField(max_length=200)
    total_price = models.IntegerField(null=True, blank=True)  
    original_price = models.IntegerField()
    product_information = RichTextField()
    model_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100)
    description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def clean(self):
        
        if self.section.name == "Top Deals Of The Day":
            if self.discount is None or self.total_price is None:
                raise ValidationError("Discount and total price are required for 'Top Deals Of The Day' products.")
        else:
           
            if self.discount is not None or self.total_price is not None:
                raise ValidationError("Only original price should be set for products in sections other than 'Top Deals Of The Day'.")

    
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)




class Product_Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    img_url = models.CharField(max_length=200)


class Additional_Information(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    specification = models.CharField(max_length=100)    
    detail = models.CharField(max_length=100)    



