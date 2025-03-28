from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import School, Employee, Application
from .serializers import SchoolSerializer, EmployeeSerializer, ApplicationSerializer

class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to allow only superusers to add a school.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsSchoolAdmin(permissions.BasePermission):
    """
    Custom permission to allow only school admins to manage their school and add employees.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin  # Only the assigned school admin can modify the school

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get_permissions(self):
        if self.action == 'create':  # Only superusers can create schools
            return [IsSuperUser()]
        return [IsSchoolAdmin()]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """
        Restrict employees to only those belonging to the admin's school.
        """
        if self.request.user.is_authenticated:
            return Employee.objects.filter(school__admin=self.request.user)
        return Employee.objects.none()

    def get_permissions(self):
        return [IsSchoolAdmin()]

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can apply to a school

    def get_queryset(self):
        """
        Filter applications by school.
        """
        school_id = self.request.query_params.get('school_id')
        if school_id:
            return Application.objects.filter(school__id=school_id)
        return Application.objects.all()
