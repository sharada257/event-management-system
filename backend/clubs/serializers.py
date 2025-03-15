from rest_framework import serializers
from .models import Club, ClubMembership

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'club_name', 'description', 'teacher', 'department']

class ClubMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubMembership
        fields = ['id', 'student', 'club', 'role', 'can_post_event', 'joined_at']