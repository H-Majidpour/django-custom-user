from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, CustomUserCreationForm
from .decorators import user_not_authenticated



@login_required
def home(request):
    return render(request, 'home-page.html')


@user_not_authenticated
def login_view(request):
    form = UserLoginForm()
    next_url = None
    
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # log in the user
            email=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get("next")
                return redirect(next_url or "/")
 
    return render(request, "login-page.html", {"form": form})


@user_not_authenticated
def register_view(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        
    return render(request, "register-page.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")


