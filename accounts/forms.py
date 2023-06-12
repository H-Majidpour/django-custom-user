from django import forms
from django.contrib.auth.forms import(
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm,
) 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

UserModel = get_user_model()



class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    class Meta:
        model = UserModel
        fields = ["email"]


class CustomUserChangeForm(UserChangeForm):
    """
    A form that allows users to change their password.
    """
    class Meta:
        model = UserModel
        fields = ["email"]
        

class UserLoginForm(AuthenticationForm):
    """
    A form for authenticating users.
    """
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        if username and password:
            try:
                self.user_cache = UserModel.objects.get(email=username)
                if self.user_cache.check_password(password):
                    self.confirm_login_allowed(self.user_cache)
                    
                else:
                    raise self.get_invalid_login_error()
            except UserModel.DoesNotExist:
                raise self.get_invalid_login_error()     
        
        return self.cleaned_data
