from dataclasses import dataclass
from typing import List
from datetime import datetime

from .embedding import NoteEmbeddingEntity
from .permission import NotePermissionEntity

@dataclass
class NoteEntity:
    """Represents one record of note.metadata"""
    note_id: int
    title: str
    updated_at: datetime
    author_id: int
    content: str
    embeddings: List[NoteEmbeddingEntity]
    permissions: List[NotePermissionEntity]
