from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced  # Compact import

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # Naming convention: Removed "Model" from class names
    list_display = ('id', 'title', 'discounted_price', 'category', 'product_image')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'locality', 'city', 'zipcode')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'razorpay_order_id', 
                    'razorpay_payment_status', 'razorpay_payment_id', 'paid')

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'product', 'quantity', 
                    'ordered_date', 'status', 'payment')
