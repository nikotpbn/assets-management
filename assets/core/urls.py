from django.urls import path
from .views import auth_login

urlpatterns = [
    path("", auth_login, name="index"),
    path("login/", auth_login, name="login"),
]
