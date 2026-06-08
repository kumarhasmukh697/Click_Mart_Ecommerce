from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'created_at', 'updated_at')
    search_fields = ('cart__user__email', 'product__name')
    ordering = ('-created_at',)


