# Event Models - events/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from clubs.models import Club
from accounts.models import Student, Coordinator
from django.utils import timezone


class Event(BaseModel):
    """
    Model for storing event information.
    """
    class EventType(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', _('Individual')
        GROUP = 'GROUP', _('Group')

    class EventStatus(models.TextChoices):
        UPCOMING = 'UPCOMING', _('Upcoming')
        ONGOING = 'ONGOING', _('Ongoing')
        COMPLETED = 'COMPLETED', _('Completed')

    class RegistrationStatus(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        CLOSED = 'CLOSED', _('Closed')

    class ApprovalStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')

    event_name = models.CharField(max_length=200)
    description = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    event_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.INDIVIDUAL)
    max_participants = models.PositiveIntegerField()
    club = models.ForeignKey('clubs.Club', on_delete=models.CASCADE, related_name='events')
    created_by = models.ForeignKey('accounts.Student', on_delete=models.SET_NULL, null=True, related_name='created_events')
    event_status = models.CharField(max_length=20, choices=EventStatus.choices, default=EventStatus.UPCOMING)
    registration_status = models.CharField(max_length=20, choices=RegistrationStatus.choices, default=RegistrationStatus.CLOSED)
    approval_status = models.CharField(max_length=20, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    
    def __str__(self):
        return f"{self.event_name} ({self.get_event_status_display()})"

    def save(self, *args, **kwargs):
        # Update event status based on dates
        now = timezone.now()
        if now < self.event_date:
            self.event_status = self.EventStatus.UPCOMING
        elif now >= self.event_date and now <= self.end_date:
            self.event_status = self.EventStatus.ONGOING
        else:
            self.event_status = self.EventStatus.COMPLETED
            self.registration_status = self.RegistrationStatus.CLOSED

        
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['event_status']),
            models.Index(fields=['approval_status']),
            models.Index(fields=['club']),
            models.Index(fields=['event_date']),
            
        ]


class EventApproval(BaseModel):
    """
    Model for tracking event approvals from coordinators.
    """
    class ApprovalStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='approvals')
    coordinator = models.ForeignKey('accounts.Coordinator', on_delete=models.CASCADE, related_name='event_approvals')
    approval_status = models.CharField(max_length=20, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    comments = models.TextField(blank=True, null=True)
    approval_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set approval date when status changes from pending
        if self.approval_status != self.ApprovalStatus.PENDING and not self.approval_date:
            self.approval_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Event: {self.event.event_name} - Status: {self.get_approval_status_display()}"

    class Meta:
        unique_together = ('event', 'coordinator')
        indexes = [
            models.Index(fields=['approval_status']),
        ]


class Group(BaseModel):
    """
    Model for storing group information for group events.
    """
    group_name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='groups')
    leader = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='led_groups')
    max_members = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.group_name} - {self.event.event_name}"

    class Meta:
        unique_together = ('group_name', 'event')


class GroupMember(BaseModel):
    """
    Model for tracking students who are part of groups for group events.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='group_memberships')
    joined_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.group.group_name}"

    class Meta:
        unique_together = ('group', 'student')


class EventRegistration(BaseModel):
    """
    Model for storing event registrations.
    """
    class RegistrationStatus(models.TextChoices):
        CONFIRMED = 'CONFIRMED', _('Confirmed')
        WAITLISTED = 'WAITLISTED', _('Waitlisted')
        CANCELLED = 'CANCELLED', _('Cancelled')

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='event_registrations')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='registrations')
    registered_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=RegistrationStatus.choices, default=RegistrationStatus.CONFIRMED)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.event.event_name} ({self.get_status_display()})"

    class Meta:
        unique_together = ('event', 'student')
        indexes = [
            models.Index(fields=['status']),
        ]


class EventAttendance(BaseModel):
    """
    Model for tracking attendance at events.
    """
    registration = models.OneToOneField(EventRegistration, on_delete=models.CASCADE, related_name='attendance')
    attended = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)