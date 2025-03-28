from django.contrib import admin
from .models import School, Employee, Application

class SchoolAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser  

admin.site.register(School, SchoolAdmin)
admin.site.register(Employee)
admin.site.register(Application)
