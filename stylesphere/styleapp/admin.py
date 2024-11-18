from django.contrib import admin
from .models import Category,Clothes,Cart,Order,Userdetails

# Register your models here.
@admin.register(Userdetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone', 'image')
    search_fields = ('user__username', 'address', 'phone')
    list_filter = ('user',)

admin.site.register(Category)
@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'description', 'image')  # Display these fields in the list view
    search_fields = ('name', 'category__name')  # Search functionality for name and category name
    list_filter = ('category',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price')  # Fields to display in the list view
    search_fields = ('user_username', 'product_name')  # Search by user's username and product's name
    list_filter = ('user', 'product')  # Filter by user and product

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total', 'created_at')  # Fields to display in the list view
    list_filter = ('created_at',)  # Filter orders by date
    search_fields = ('user_username', 'product_name')  # Allow searching by user and product
    ordering = ('-created_at',)  # Order the list by most recent orders

