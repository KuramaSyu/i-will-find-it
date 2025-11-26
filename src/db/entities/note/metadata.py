from dataclasses import dataclass

@dataclass
class NoteMetadataEntity:
    """Represents one record of note.metadata"""
    note_id: int
    title: str
    author_id: int
