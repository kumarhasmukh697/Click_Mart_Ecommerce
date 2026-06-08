from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from .serializer import OrderSerializer, OrderItemSerializer

# Create your views here.


# Get last four orders for the authenticated user and place a new order for the authenticated user
class OrderView(APIView):
    permission_classes = [IsAuthenticated]

   
    def get(self, request):
        # get last four orders for the authenticated user
        orders = Order.objects.filter(user=request.user).order_by('-created_at')[:4]
        if not orders.exists():
            return Response({"detail": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    

    # place a new order for the authenticated user
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        # Create order from cart items
        shipping_data = request.data.get('shippingAddress', {})
        order = Order.objects.create(
            user=request.user,
            subtotal=cart.subtotal,
            tax=cart.tax,
            total=cart.total,
            address=shipping_data.get('address', ''),
            phone_number=shipping_data.get('phone', ''),
            city=shipping_data.get('city', ''),
            state=shipping_data.get('state', ''),
            zip_code=shipping_data.get('zipcode', '')
        )
        for item in cart.items.all():
            # create order item for each cart item only if stock is available
            if item.product.stock < item.quantity:
                print("Not enough stock for", item.product.name)
                order.delete()  # delete the created order if stock is not available
                return Response({"detail": f"Not enough stock for {item.product.name}."}, status=status.HTTP_400_BAD_REQUEST)
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                subtotal=item.product.price * item.quantity,
                tax=((item.product.price * item.quantity) * item.product.tax_percentage) / 100,
                total=(item.product.price * item.quantity) + ((item.product.price * item.quantity) * item.product.tax_percentage) / 100
            )
            # decreae product stock
            item.product.stock = item.product.stock - item.quantity
            item.product.save()

        # clear the cart
        cart.items.all().delete()
            
        return Response({"detail": "Order placed successfully."}, status=status.HTTP_201_CREATED)



# Get all orders for the authenticated user       
class MyallOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        if not orders.exists():
            return Response({"detail": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)   


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


