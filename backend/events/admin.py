from django.contrib import admin
from .models import Event, EventApproval, Group, GroupMember, EventRegistration, EventAttendance

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date', 'end_date', 'location', 'event_type', 'event_status', 'registration_status', 'approval_status', 'club']
    search_fields = ['event_name', 'club__club_name']

@admin.register(EventApproval)
class EventApprovalAdmin(admin.ModelAdmin):
    list_display = ['event', 'coordinator', 'approval_status', 'approval_date']
    search_fields = ['event__event_name', 'coordinator__user__email']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'event', 'leader', 'max_members']
    search_fields = ['group_name', 'event__event_name', 'leader__user__email']

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['group', 'student', 'joined_at']
    search_fields = ['group__group_name', 'student__user__email']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'student', 'group', 'registered_at', 'status']
    search_fields = ['event__event_name', 'student__user__email', 'group__group_name']

@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ['registration', 'attended', 'check_in_time']
    search_fields = ['registration__event__event_name', 'registration__student__user__email']