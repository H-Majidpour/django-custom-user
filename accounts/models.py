import random
import string

from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager
from .validators import UsernameValidator, AgeValidator


def generate_unique_random_username(length=15):
    """
    Generate a unique random username of the given length.
    """
    characters = string.ascii_lowercase + string.digits + "_"
    
    # Generate a random username
    random_username = "".join(random.choice(characters) for _ in range(length))
    
    # Check valid username
    while True:
        # Check if the username starts or ends with an underscore.
        if random_username.startswith("_") or random_username.endswith("_"):
            random_username = "".join(random.choice(characters) for _ in range(length))
            
        # Check if the username starts with a digit.
        if random_username[0].isdigit():
            random_username = "".join(random.choice(characters) for _ in range(length))

        return random_username


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), unique=True)
    username = models.CharField(
        _("Username"),
        unique=True,
        max_length=15,
        help_text= _(
            "You can use a-z, 0-9 and underscore. " 
            "Minimum length in 5 character."
        ),
        validators=[
            UsernameValidator(),
            MinLengthValidator(5),
        ]
    )
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
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_unique_random_username()
        super().save(*args, **kwargs)
    
    def get_username(self):
        """Return the username for this User."""
        return self.username
    
    def clean(self):
        self.username = self.username.lower()
        self.username = self.normalize_username(self.username)
        
        
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(_("First name"), max_length=30, null=True)
    last_name = models.CharField(_("Last name"), max_length=30, null=True)
    profile_image = models.ImageField(_("Profile image"), upload_to="profile_image/", null=True, blank=True)
    bio = models.TextField(_("Biography"), null=True)
    location = models.CharField(_("Location"), max_length=100, null=True)
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER_CHOICES, null=True)
    birth_date = models.DateField(_("Date of birth"), validators=[AgeValidator()], null=True)
    
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