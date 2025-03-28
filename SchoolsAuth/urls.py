from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, EmployeeViewSet, ApplicationViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('api/', include(router.urls)),  # Include all registered routes
]
