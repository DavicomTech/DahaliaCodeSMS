from django.db import models
from django.contrib.auth.models import User
import uuid

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
        return f"/schools/{self.school_id}/"
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
