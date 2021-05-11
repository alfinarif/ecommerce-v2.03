from django.urls import path
from order import views

urlpatterns = [
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart_view, name='cart'),
    path('remove-item/<int:pk>/', views.remove_item_from_cart, name='remove_item'),
    path('increase/<int:pk>/', views.increase_cart, name='increase'),
    path('decrease/<int:pk>/', views.decrease_cart, name='decrease'),
    path('wishlist-add/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove-coupon/', views.delete_session_data, name='remove_coupon'),
]
