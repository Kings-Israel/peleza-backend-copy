from django.urls import path
from rest_framework import views
from .views import Login, Profile, Register

urlpatterns = [
    path("login/", Login.as_view()),
    path("register/", Register.as_view()),
    path("profile/", Profile.as_view()),
]
