from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login', AuthenticationAPI.as_view()),
    path('signup', RegistrationAPI.as_view()),
    path('products', ProductAPI.as_view()),
    path('cart', CartAPI.as_view()),
    path('cart/<int:pk>', CartAPI.as_view()),
    path('order', OrderAPI.as_view()),
    path('logout', LogoutView.as_view()),
    path('product', ProductAPI.as_view()),
    path('product/<int:pk>', ProductAPI.as_view()),
]