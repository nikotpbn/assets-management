from django.urls import path
from .views import auth_login, auth_logout, password_recover, password_recover_new

urlpatterns = [
    path("", auth_login, name="index"),
    path("login/", auth_login, name="login"),
    path("logout/", auth_logout, name="logout"),
    path("password/recover/", password_recover, name="password-recover"),
    path("password/recover/new/", password_recover_new, name="password-recover-new"),
]
