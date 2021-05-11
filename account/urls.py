
from django.urls import path
from account import views
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('is_read_notific/', views.is_read_notific, name='notific'),
]
