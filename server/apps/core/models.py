import uuid

from django.db import models


class UUIDMixin(models.Model):
    id = models.UUIDField(
        "uuid4",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(
        "updated at",
        auto_now=True,
    )

    class Meta:
        abstract = True
