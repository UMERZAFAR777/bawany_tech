from django.contrib import admin
from product.models import *
# Register your models here.

class Product_Images(admin.TabularInline):
    model = Product_Image

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images, Additional_Informations)
    list_display = ('product_name', 'category', 'original_price', 'total_price', 'section') 
    list_display_links = ('product_name',) 
    list_editable = ('original_price', 'total_price', 'section') 



admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(Time)


