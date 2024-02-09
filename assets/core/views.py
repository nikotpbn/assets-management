from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def auth_login(request):
    if request.user.is_authenticated:
        return redirect("asset-list")

    email = None
    password = None
    msg = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password", None)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("asset-list")

        msg = 'Email ou senha incorretos.'

    return render(request, "login.html", {'email': email, 'error': msg})


def auth_logout(request):
    logout(request)
    print('brooo')
    return redirect("index")
