from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrb.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, EmailValidator
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.conf import settings
import logging
import requests
from io import BytesIO

class CustomUserManager(BaseUserManager):
    def create(self, validated_data):
        try:
            email = validated_data('school_email')
            password = validated_data('password')
            school_name = validated_data('school_name')

            user = User.objects.create_user(
                email=email,
                password=password,
                school_name=school_name,
                **{k: v for k, v in validated_data.items() if k not in ['school_email', 'password', 'school_name']}
            )

            logging.info(f"User created successfully: {email}")

        except Exception as e:
            logging.error(f"Error during user registration: {e}")
            raise ValidationError("User registration failed.")
        return user
    
    def create_superuser(self, email, )
class School(models.Model):
    school_id = models.CharField(max_length=10, unique=True, editable=False)
    school_name = models.CharField(max_length=255)
    logo = models.ImageField(default='default.jpeg', upload_to='logos')
    address = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='school')

    class Meta:
        indexes = [
            models.Index(fields=['school_name']),  # Index for filtering by school name
            models.Index(fields=['school_id']),  # Index on unique school ID
        ]

    def save(self, *args, **kwargs):
        if not self.school_id:
            self.school_id = str(uuid.uuid4())[:10]  # Generate a unique ID
        super().save(*args, **kwargs)

    def __str__(self):
        return self.school_name
    def get_absolute_url(self):
        return f"/{self.school_name}/"
    def get_logo_url(self):
        if self.logo:
            return self.logo.url
        return None
    def get_address(self):
        if self.address:
            return self.address
        return None
    def get_user(self):
        if self.user:
            return self.user.username
        return None

