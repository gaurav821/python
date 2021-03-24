from django.contrib import admin
from .models import Customer,Product,orderItem,Order,ShippingAddress
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(orderItem)
admin.site.register(ShippingAddress)

