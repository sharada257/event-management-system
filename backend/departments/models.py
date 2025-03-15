from django.db import models
from core.models import BaseModel

class Department(BaseModel):
    """
    Model for storing department information.
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"