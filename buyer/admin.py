from django.contrib import admin

# Register your models here.
from buyer.models import *

# class BuyerAdmin(admin.ModelAdmin):
#     list_display = ("id", "first_name", "last_name", "total_products",'total_amount')

#     def display_product_names(self, obj):
#         names = obj.product_names.replace(",", ", ")  
#         return names[:30] + "..." if len(names) > 30 else names 
#     display_product_names.short_description = "Product Names"

# admin.site.register(Buyer, BuyerAdmin)



class OrderItemInline(admin.TabularInline): 
    model = OrderItem
    extra = 0  


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0  
    inlines = [OrderItemInline]  


class BuyerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "total_products", "total_amount")
    inlines = [OrderInline]
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "order_total", "status", "created_at")
    inlines = [OrderItemInline]  

admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Order, OrderAdmin)


