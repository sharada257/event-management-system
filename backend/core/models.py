# Core Models - core/models.py
from django.db import models
import uuid
from django.utils import timezone


class BaseModel(models.Model):
    """
    Base model to provide common fields for all models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True