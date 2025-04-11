# store/admin.py
from django.contrib import admin
from .models import Category, Product, Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'in_stock', 'is_featured', 'created']
    list_filter = ['in_stock', 'is_featured', 'category']
    list_editable = ['price', 'in_stock', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created', 'updated']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']