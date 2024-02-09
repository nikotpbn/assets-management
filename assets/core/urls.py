from django.urls import path
from .views import auth_login, auth_logout

urlpatterns = [
    path("", auth_login, name="index"),
    path("login/", auth_login, name="login"),
    path("logout/", auth_logout, name="logout"),
]
