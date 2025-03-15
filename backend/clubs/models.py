from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Club(BaseModel):
    """
    Model for storing club information.
    """
    club_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    teacher = models.ForeignKey('accounts.Teacher', on_delete=models.SET_NULL, null=True, related_name='supervised_clubs')
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, 
                                  related_name='clubs', blank=True)

    def __str__(self):
        return self.club_name


class ClubMembership(BaseModel):
    """
    Model for tracking club memberships and roles within clubs.
    """
    class MembershipRole(models.TextChoices):
        PRESIDENT = 'PRESIDENT', _('President')
        VICE_PRESIDENT = 'VICE_PRESIDENT', _('Vice President')
        BOARD_MEMBER = 'BOARD_MEMBER', _('Board Member')
        TREASURER = 'TREASURER', _('Treasurer')
        CLUB_MEMBER = 'CLUB_MEMBER', _('Club Member')
        VOLUNTEER = 'VOLUNTEER', _('Volunteer')

    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='club_memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=MembershipRole.choices, default=MembershipRole.CLUB_MEMBER)
    can_post_event = models.BooleanField(default=False)
    joined_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Automatically set can_post_event based on role
        if self.role in [self.MembershipRole.PRESIDENT, self.MembershipRole.VICE_PRESIDENT]:
            self.can_post_event = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.club.club_name} ({self.get_role_display()})"

    class Meta:
        unique_together = ('student', 'club')
        indexes = [
            models.Index(fields=['student', 'club']),
            models.Index(fields=['role']),
        ]