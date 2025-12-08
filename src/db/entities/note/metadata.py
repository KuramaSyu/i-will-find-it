from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from asyncpg import Record

from .embedding import NoteEmbeddingEntity
from .permission import NotePermissionEntity
from api.undefined import *

@dataclass
class NoteEntity:
    """Represents one record of note.metadata"""
    note_id: UndefinedOr[int]
    title: UndefinedNoneOr[str]
    updated_at: UndefinedNoneOr[datetime]
    author_id: UndefinedNoneOr[int]
    content: UndefinedNoneOr[str]
    embeddings: List[NoteEmbeddingEntity]
    permissions: List[NotePermissionEntity]

    @staticmethod
    def from_record(record: Record) -> "NoteEntity":
        return NoteEntity(
            note_id=record.get("id", UNDEFINED),
            title=record.get("title", UNDEFINED),
            updated_at=record.get("updated_at", UNDEFINED),
            author_id=record.get("author_id", UNDEFINED),
            content=record.get("content", UNDEFINED),
            embeddings=[],
            permissions=[]
        )
