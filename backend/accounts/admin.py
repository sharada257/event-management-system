from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Coordinator

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'is_active', 'created_at', 'updated_at']
    search_fields = ['email', 'role']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'year', 'department', 'section']
    search_fields = ['user__email', 'department__name']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']
    search_fields = ['user__email', 'department__name']

@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']
    search_fields = ['user__email', 'department__name']