from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q

from .forms import UserLoginForm, CustomUserCreationForm
from .decorators import user_not_authenticated
from .token import account_activation_token


UserModel = get_user_model()



def send_confirmation_email(request, user, to_email):
    """Sends a confirmation email to the user."""
    mail_subject = "Activate your account"
    message = render_to_string("activate_email.html", {
        "user": user,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        # "protocol": "https" if request.is_secure else "http",
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Please check your email inbox <b>{to_email}</b> and click \
            on the activation link to confirm your registration. <strong>Note</strong>: Check your spam folder.")
    else:
        messages.error(request, f"Problem sending email to {to_email}, check if you typed it correctly.")


def activate(request, uidb64, token):
    """
    Activates a user account.
    First, the function decodes the user ID from base64, then the function
    gets the user from the database by user ID.
    
    If the user is not found, the function returns None.
    
    Next, the function checks if the activation token is valid,
    If the token is valid, the function activates the user account.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Your account has been successfully verified. "
            "Now you can login your account."
        )
        return redirect("/login/")
    else:
        messages.error(request, "The confirmation email has expired.")
    return redirect("/")


@user_not_authenticated
def resend_confirmation_email(request):
    user_info = request.session.get("user_info")
    if user_info:
        try:
            user = UserModel.objects.get(Q(email=user_info) | Q(username=user_info))
            print(user_info)
            send_confirmation_email(request, user, user.email)
            request.session.pop("user_info")
            return redirect("/")
        except UserModel.DoesNotExist:
            return redirect("/")
    return redirect("/")


@user_not_authenticated
def login_view(request):
    form = UserLoginForm()
    next_url = None
    
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # log in the user
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                next_url = request.POST.get("next")
                return redirect(next_url or "/")
        else:
            handle_auth_error(request, form)
        
    return render(request, "login-page.html", {"form": form})


@user_not_authenticated
def register_view(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_confirmation_email(request, user, user.email)
            return redirect("/")
        else:
            handle_auth_error(request, form)

    return render(request, "register-page.html", {"form": form})


def handle_auth_error(request, form):
    errors = form.errors.as_data()
    for field, error_list in errors.items():
        for error in error_list:
            if error.code == "inactive":
                user_info = form.cleaned_data["username"]
                request.session["user_info"] = user_info
                url = "<a href='/resend_confirmation' class='alert-link'>Click</a>"
                messages.warning(request, f"Your account is inactive. \
                    Please {url} to send the confirmation link.")
            else:
                message = error.message
                params = error.params
                messages.error(request, message if not params else message % params)


@login_required
def home(request):
    return render(request, 'home-page.html')           
                

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")


