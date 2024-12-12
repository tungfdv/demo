from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Company(models.Model):
    name = models.CharField(max_length=255)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, default="en")
    language = models.CharField(
        max_length=10, choices=[("en", ("English")), ("fr", ("French"))], default="en"
    )

    def __str__(self):
        return self.user.email
