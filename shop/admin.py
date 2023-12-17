from django.contrib import admin
from .models import Product, Customer, Cart, CartItem, Order
# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['name_to_deliver', 'is_deliver']
    list_display = ['name_to_deliver', 'is_deliver', 'total']
    inlines = [CartItemInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    list_filter = ['category']

admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)