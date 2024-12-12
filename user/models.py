from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for UserProfile"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    """Database model for users in the system"""

    user_id = models.CharField(max_length=255, unique=True)
    kana_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.IntegerField()
    role = models.CharField(max_length=255)
    label = models.CharField(max_length=255, null=True, blank=True)
    group = models.IntegerField()
    qrcode = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_id", "company", "role", "group", "username"]

    def __str__(self):
        """Return string representation of our user"""
        return f"{self.email} ({self.username})"
