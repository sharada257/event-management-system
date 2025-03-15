from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from core.models import BaseModel
from departments.models import Department
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
        ('COORDINATOR', 'Coordinator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


class Student(BaseModel):
    """
    Model for storing student-specific information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    year = models.PositiveIntegerField()
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='students')
    section = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department.name} (Year {self.year}, Section {self.section})"


class Teacher(BaseModel):
    """
    Model for storing teacher-specific information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='teachers')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department.name}"


class Coordinator(BaseModel):
    """
    Model for storing coordinator-specific information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coordinator_profile')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='coordinators',
                                   null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Coordinator"