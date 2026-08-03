from __future__ import annotations

from django.db import transaction

from ai_agent.llm.gemini_embedding_client import GeminiEmbeddingClient
from ai_agent.models import Document, DocumentChunk
from ai_agent.rag.chunking.service import ChunkingService
from ai_agent.rag.indexing.exceptions import IndexingError


class IndexingService:
    """Indexes documents into vectorized document chunks."""

    def __init__(
        self,
        chunking_service: ChunkingService,
        embedding_client: GeminiEmbeddingClient,
    ) -> None:
        self._chunking_service = chunking_service
        self._embedding_client = embedding_client

    @transaction.atomic
    def index(
        self,
        document: Document,
    ) -> None:
        """
        Index a document by chunking its content, generating embeddings,
        and persisting the resulting document chunks.
        """
        chunks = self._chunking_service.chunk(
            document.content,
        )

        if not chunks:
            document.chunks.all().delete()
            return

        texts = [chunk.text for chunk in chunks]

        embeddings = self._embedding_client.embed_many(
            texts,
        )

        if len(chunks) != len(embeddings):
            raise IndexingError(
                "The number of generated embeddings does not match the number of chunks.",
            )

        document.chunks.all().delete()

        document_chunks = [
            DocumentChunk(
                document=document,
                text=chunk.text,
                embedding=embedding,
                metadata=chunk.metadata,
                chunk_index=chunk.chunk_index,
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
                strict=True,
            )
        ]

        DocumentChunk.objects.bulk_create(
            document_chunks,
        )
