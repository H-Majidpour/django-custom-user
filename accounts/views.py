from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import UserLoginForm


def home(request):
    return render(request, 'home-page.html')


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                # log in the user
                user = form.get_user()           
                login(request, user)
                if next_url := request.POST.get("next"):
                    return redirect(next_url)
                return redirect("/home/")
        else:
            form = UserLoginForm()
        return render(request, "login-page.html", {"form": form})
    else:
        return redirect("/home/")
