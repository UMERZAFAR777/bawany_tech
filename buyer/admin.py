from django.contrib import admin

# Register your models here.
from buyer.models import *

class BuyerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "total_products",'total_amount')

    def display_product_names(self, obj):
        names = obj.product_names.replace(",", ", ")  
        return names[:30] + "..." if len(names) > 30 else names 
    display_product_names.short_description = "Product Names"

admin.site.register(Buyer, BuyerAdmin)




