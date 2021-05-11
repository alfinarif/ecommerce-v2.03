from django.contrib import admin
from order.models import Cart, Order, Wishlist


admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)
