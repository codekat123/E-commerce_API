from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai_agent.rag.chunk import Chunk


class ChunkingService:
    DEFAULT_CHUNK_SIZE = 1000
    DEFAULT_CHUNK_OVERLAP = 200

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk(self, text: str) -> list[Chunk]:
        if not text.strip():
            return []

        documents = self._splitter.create_documents([text])

        return [
            Chunk(
                text=document.page_content,
                chunk_index=index,
            )
            for index, document in enumerate(documents)
        ]
