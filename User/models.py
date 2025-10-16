from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=40)
    country = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.line1}, {self.city}, {self.country}"


class User(AbstractUser):
    class Role(models.TextChoices):
        Customer = "customer", "Customer"
        Admin = "admin", "Admin"
        Staff = "staff", "Staff"

    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    role = models.CharField(max_length=100, choices=Role.choices, default=Role.Customer)
    # Optional relation to Address (use null/blank to avoid required field on create)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email