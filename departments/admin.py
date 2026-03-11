from django.contrib import admin
from .models import Department, AgentDepartment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "is_active")
    search_fields = ("name", "code")

@admin.register(AgentDepartment)
class AgentDepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "agent", "department", "assigned_at")
    list_filter = ("department",)