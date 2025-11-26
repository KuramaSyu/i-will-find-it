from dataclasses import dataclass
from typing import Sequence


@dataclass
class NoteEmbeddingEntity:
    """Represents one record of note.embedding"""
    note_id: int
    model: str
    embedding: Sequence[float]
