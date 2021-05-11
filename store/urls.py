from django.urls import path
from store import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('category/<int:pk>/', views.category_product, name='category'),
    path('quickview/<int:pk>/', views.category_quickview, name='quickview'),
]
