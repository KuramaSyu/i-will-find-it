from dataclasses import dataclass

from api.undefined import UndefinedOr

@dataclass
class NotePermissionEntity:
    """Represents one record of note.metadata"""
    note_id: UndefinedOr[int]
    role_id: UndefinedOr[int]
