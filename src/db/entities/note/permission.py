from dataclasses import dataclass

@dataclass
class NotePermissionEntity:
    """Represents one record of note.metadata"""
    note_id: int
    role_id: int
