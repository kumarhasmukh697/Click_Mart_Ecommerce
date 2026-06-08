from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from products.models import Product
from .serializer import CartSerializer, CartItemSerializer

# Create your views here.

class CartView(APIView):
    # Only logged-in users can access
    permission_classes = [IsAuthenticated]
    def get(self,request):
         # Get or create cart for the currently logged-in user
        cart,created = Cart.objects.get_or_create(user=request.user)
         # Convert cart object to JSON
        serializer = CartSerializer(cart)
         # Return the cart data as JSON response
        return Response(serializer.data)
    



class AddToCartView(APIView):
    # Only logged-in users can access
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # get the product id and quantity from the frontend
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

       
        if not product_id or not quantity:
            return Response({'error': 'Product ID and quantity are required'}, status=400)
        

        product = Product.objects.get(id=product_id)

        # handle the functionality if cart is not created than create it also handle if cart is already created than add the product to the cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartSerializer(cart)

        return Response({'message': 'Product added to cart successfully'}, status=200)
    


class ManageCartItemView(APIView):
    permission_classes = [IsAuthenticated]
   

    def patch(self,request,item_id):
      
        change = request.data.get('change')
    
        if change not in [1, -1]:
            return Response({'error': 'Invalid action'}, status=400)
        
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=404)
        
        if change == 1:
            cart_item.quantity += 1
        elif change == -1:
            cart_item.quantity -= 1
        
        if cart_item.quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Cart item removed'}, status=200)
        
        cart_item.save()
        return Response({'message': 'Cart item updated'}, status=200)


    def delete(self,request,item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        if cart_item:
            cart_item.delete()
            return Response({'message': 'Cart item removed'}, status=200)
        return Response({'error': 'Cart item not found'}, status=404)