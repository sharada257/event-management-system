from django.contrib import admin
from .models import Club, ClubMembership

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['club_name', 'description', 'teacher']
    search_fields = ['club_name', 'teacher__user__email']

@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ['student', 'club', 'role', 'can_post_event', 'joined_at']
    search_fields = ['student__user__email', 'club__club_name', 'role']