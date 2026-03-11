from django.contrib import admin
from .models import User, StudentProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "full_name", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "full_name", "email")

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "student_id", "user", "phone")
    search_fields = ("student_id", "user__username", "user__full_name")