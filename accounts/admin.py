from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("id", "username", "full_name", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("full_name", "email", "first_name", "last_name")}),
        ("Role Info", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "full_name", "email", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("username", "full_name", "email")
    ordering = ("id",)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "student_id", "user", "phone")
    search_fields = ("student_id", "user__username", "user__full_name")