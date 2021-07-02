from django.urls import path
from notification import views

urlpatterns = [
    path('seen/', views.seen_notify, name='is_seen'),
]
