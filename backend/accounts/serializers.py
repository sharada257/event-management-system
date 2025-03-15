from rest_framework import serializers
from .models import User, Student, Teacher, Coordinator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'created_at', 'updated_at']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user', 'year', 'department', 'section']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'department']

class CoordinatorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Coordinator
        fields = ['user']