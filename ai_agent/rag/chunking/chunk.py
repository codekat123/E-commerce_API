from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Chunk:
    text: str
    chunk_index: int
    metadata: dict[str, object] = field(default_factory=dict)
