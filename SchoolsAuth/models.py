from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
import uuid

class School(models.Model):
    school_id = models.CharField(max_length=10, unique=True, editable=False)
    school_name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(default='default.jpeg', upload_to='logos')
    address = models.CharField(max_length=255)
    unique_url = models.SlugField(unique=True)  # Unique URL for student applications
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_schools')

    class Meta:
        indexes = [
            models.Index(fields=['school_name']),
            models.Index(fields=['school_id']),
            models.Index(fields=['unique_url']),
        ]
        permissions = [
            ("can_add_school", "Can add a new school"),
            ("can_manage_school", "Can manage school details"),
        ]

    def save(self, *args, **kwargs):
        if not self.school_id:
            self.school_id = str(uuid.uuid4())[:10]
        if not self.unique_url:
            self.unique_url = self.school_name.lower().replace(" ", "-")  # Generate a slug URL
        super().save(*args, **kwargs)

    def __str__(self):
        return self.school_name

    def get_absolute_url(self):
        return f"/schools/{self.unique_url}/"

class Employee(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="employees")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("can_add_employee", "Can add employees to school"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Application(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending")
    
    def __str__(self):
        return f"{self.full_name} - {self.school.school_name}"
