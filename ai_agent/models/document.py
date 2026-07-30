from __future__ import annotations

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Document(models.Model):
    vendor = models.ForeignKey(
        "users.Vendor",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveBigIntegerField()

    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    checksum = models.CharField(
        max_length=64,
    )

    embedding_model = models.CharField(
        max_length=100,
    )

    indexed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("id",)

        indexes = [
            models.Index(
                fields=("vendor",),
            ),
            models.Index(
                fields=("content_type", "object_id"),
            ),
        ]

    def __str__(self) -> str:
        return f"Document #{self.pk}"
