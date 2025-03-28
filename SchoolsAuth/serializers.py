from rest_framework import serializers
from django.contrib.auth.models import User
from .models import School, Employee, Application

class SchoolSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_superuser=True))  # Only allow superusers as school admins

    class Meta:
        model = School
        fields = ['id', 'school_id', 'school_name', 'logo', 'address', 'unique_url', 'admin']
        read_only_fields = ['school_id', 'unique_url']  # Auto-generated fields

class EmployeeSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = Employee
        fields = ['id', 'school', 'user', 'role']

    def validate(self, data):
        """
        Ensure that only a school's admin can add employees.
        """
        request = self.context['request']
        if not request.user.is_authenticated or request.user != data['school'].admin:
            raise serializers.ValidationError("Only the school's admin can add employees.")
        return data

class ApplicationSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = Application
        fields = ['id', 'school', 'full_name', 'email', 'phone', 'status']
        read_only_fields = ['status']  # Default status is 'Pending'
