from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'created_at', 'status')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)
