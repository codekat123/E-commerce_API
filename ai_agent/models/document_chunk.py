from __future__ import annotations

from django.db import models
from pgvector.django import HnswIndex, VectorField

from .document import Document


class DocumentChunk(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks",
    )

    text = models.TextField()

    embedding = VectorField(
        dimensions=768,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    chunk_index = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("chunk_index",)

        constraints = [
            models.UniqueConstraint(
                fields=("document", "chunk_index"),
                name="unique_document_chunk_index",
            ),
        ]

        indexes = [
            models.Index(
                fields=("document",),
            ),
            HnswIndex(
                name="document_chunk_embedding_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
            ),
        ]

    def __str__(self) -> str:
        return f"DocumentChunk(document={self.document_id}, chunk={self.chunk_index})"
