from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .views import register_user  # Import the registration API view

# Function to render the registration page
def register_page(request):
    return render(request, "register.html")

urlpatterns = [
    path("register/", register_page, name="register_page"),  # Serve the registration page
    path("api/register/", register_user, name="register_user"),  # API endpoint for user registration
]
