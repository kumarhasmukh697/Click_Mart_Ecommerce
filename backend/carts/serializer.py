from .models import Cart, CartItem
from rest_framework import serializers


# Serializer for CartItem with product name included
class CartItemSerializer(serializers.ModelSerializer):
    # to get the product name related to the cart item
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    tax_percentage = serializers.DecimalField(source='product.tax_percentage', max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = '__all__'



# Serializer for Cart with nested CartItemSerializer to include cart items in the cart representation
class CartSerializer(serializers.ModelSerializer):
    # nested serializer to get the cart items related to the cart
    items = CartItemSerializer(many=True, read_only=True)
    # get total_quantity from Cart.total_quantity property
    total_quantity = serializers.IntegerField(read_only=True)

    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tax = serializers.DecimalField(max_digits=5, decimal_places=2,read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'