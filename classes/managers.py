from django.db import models


class ExcludeDeletedObjectsManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().exclude(status="DELETED").order_by("-created_at")
    
class IncludeDeletedObjectsManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()