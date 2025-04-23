from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),

]
