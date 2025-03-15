from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventApprovalViewSet, GroupViewSet, GroupMemberViewSet, EventRegistrationViewSet, EventAttendanceViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'event-approvals', EventApprovalViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'group-members', GroupMemberViewSet)
router.register(r'event-registrations', EventRegistrationViewSet)
router.register(r'event-attendances', EventAttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]