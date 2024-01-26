from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate


# Create your views here.
def auth_login(request):
    if request.user.is_authenticated:
        return redirect('asset-list')

    if request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("asset-list")

    return render(request, "login.html")
