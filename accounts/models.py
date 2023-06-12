from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import date
from django.core.exceptions import ValidationError

from .managers import CustomUserManager


def validate_user_age(birthdate):
    """Validates the age of a user."""
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 15:
        raise ValidationError("Sorry, you must be at least 15 years old to use this service :)")
    return age


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), unique=True)
    is_active = models.BooleanField(_("Is active"), default=False)
    is_staff = models.BooleanField(_("Staff status"), default=False)
    date_joined = models.DateField(_("Date joined"), default=timezone.now)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    class Meta:
        ordering = ["-date_joined"]
    
    def __str__(self):
        return self.email
    
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(_("Username"), max_length=50, unique=True, null=True)
    first_name = models.CharField(_("First name"), max_length=30, null=True)
    last_name = models.CharField(_("Last name"), max_length=30, null=True)
    profile_image = models.ImageField(_("Profile image"), upload_to="profile_image/", null=True, blank=True)
    bio = models.TextField(_("Biography"), null=True)
    location = models.CharField(_("Location"), max_length=100, null=True)
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER_CHOICES, null=True)
    birth_date = models.DateField(_("Date of birth"), validators=[validate_user_age], null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def get_full_name(self):
        """
        Return the first_name plus last_name,  with a space in between
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    def __str__(self):
        return self.user.email
    

@receiver(post_save, sender=User)
def create_user_profile(sender, created, instance, **kwargs):
    """
    Create a profile for the user automatically when a new user is created.
    """
    if created:
        Profile.objects.create(user=instance)