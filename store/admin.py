from django.contrib import admin
from .models import Product,Cart,Order, OrderItem,Wishlist, Category

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(Category)