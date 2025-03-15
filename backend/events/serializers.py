from rest_framework import serializers
from .models import Event, EventApproval, Group, GroupMember, EventRegistration, EventAttendance

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_name', 'description', 'published_at', 'event_date', 'end_date', 'location', 'event_type', 
                  'max_participants', 'club', 'created_by', 'event_status', 'registration_status', 'approval_status']

class EventApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventApproval
        fields = ['id', 'event', 'coordinator', 'approval_status', 'comments', 'approval_date']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'event', 'leader', 'max_members']

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['id', 'group', 'student', 'joined_at']
class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'student', 'group', 'registered_at', 'status']

class EventAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendance
        fields = ['id', 'registration', 'attended', 'check_in_time']