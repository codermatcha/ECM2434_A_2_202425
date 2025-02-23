from django.urls import path
from django.shortcuts import render
from .views import register_user, login_user, get_user_profile # ✅ Ensure these functions exist in views.py

def home_page(request):
    return render(request, "home.html")

def register_page(request):
    return render(request, "register.html")

def login_page(request):
    return render(request, "login.html")  


urlpatterns = [
    path("", home_page, name="home"),  # Home page
    path("register/", register_page, name="register_page"),  # Register page
    path("login/", login_page, name="login_page"),  # Login page
    path("api/register/", register_user, name="register_user"),  # Register API
    path("api/login/", login_user, name="login_user"),  # ✅ Login API
    path("api/profile/", get_user_profile, name="user_profile"),  # ✅ Profile API

]
