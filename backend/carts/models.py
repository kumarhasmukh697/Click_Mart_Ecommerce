from django.db import models
from django.conf import settings
from products.models import Product
from decimal import Decimal

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.email
    
    @property
    def subtotal(self):
        subtotal = Decimal(0.00)
        for item in self.items.all():
            subtotal = subtotal + (item.product.price * item.quantity)
        return subtotal

    @property
    def tax(self):
        tax = Decimal(0.00)
        for item in self.items.all():
            tax = tax + ((item.product.price * item.quantity)*(item.product.tax_percentage))/100
        return tax
    
    @property
    def total(self):
        return self.subtotal + self.tax


    @property
    def total_quantity(self):
        count = 0
        for item in self.items.all():
            count = count + item.quantity
        return count
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} quantity of {self.product.name} in {self.cart.user.email}'s cart"
