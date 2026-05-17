from django.contrib import admin
from server.apps.departments.models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'hired_at')
    list_filter = ('department', 'hired_at')
    search_fields = ('full_name', 'position')
    ordering = ('-created_at',)