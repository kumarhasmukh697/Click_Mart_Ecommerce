from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from products.views import ProductDetailView, ProductListCreateView ,CategoryDetailView, CategoryListCreateView
from users.views import RegisterUserView,ProfileView
from carts.views import CartView,AddToCartView,ManageCartItemView
from orders.views import OrderView,OrderDetailView,MyallOrdersView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # user api
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('profile/', ProfileView.as_view(), name='user_profile'),


    
    #product api
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product_detail'),


    #cart api
    path('cart/', CartView.as_view(), name='cart_list_create'),
    path('cart/add/',AddToCartView.as_view(), name='add_to_cart'),
    path('cart/items/<int:item_id>/',ManageCartItemView.as_view(), name='manage_cart_item'),



    # order api
    path('orders/', OrderView.as_view(), name='order_list_create'),
    path('orders/myallorders/',MyallOrdersView.as_view(), name='my_all_orders'),
    path('orders/place/', OrderView.as_view(), name='place_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    
]