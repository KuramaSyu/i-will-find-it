from typing import Any, Dict
from google.protobuf.timestamp_pb2 import Timestamp

from api.undefined import UNDEFINED
from db.entities.note.metadata import NoteEntity
from db.repos.note.note import SearchType
from grpc_mod.converter.dict_helper import drop_except_keys
from grpc_mod.proto.note_pb2 import GetSearchNotesRequest, MinimalNote, Note, NoteEmbedding, NotePermission
from grpc_mod.converter import drop_undefined
from utils import asdict



def to_grpc_note(note_entity: NoteEntity) -> Note:
    """Converts a NoteEntity to a gRPC Note message."""

    assert note_entity.note_id is not None
    assert note_entity.title is not None
    assert note_entity.content is not None
    assert note_entity.author_id is not None

    updated_at_ts = Timestamp()
    if note_entity.updated_at:
        updated_at_ts.FromDatetime(note_entity.updated_at)

    basic_args = drop_undefined(
        drop_except_keys(
            asdict(note_entity), 
            {"note_id", "title", "content", "author_id"}
        )
    )
    basic_args["id"] = basic_args.pop("note_id")

    return Note(
        **basic_args,
        updated_at=updated_at_ts,
        embeddings=[
            NoteEmbedding(model=e.model, embedding=e.embedding)
            for e in note_entity.embeddings
        ],
        permissions=[
            NotePermission(role_id=p.role_id) for p in note_entity.permissions
        ],
    )

def to_grpc_minimal_note(note_entity: NoteEntity) -> MinimalNote:
    """Converts a NoteEntity to a gRPC MinimalNote message."""

    assert note_entity.note_id is not None
    assert note_entity.title is not None
    assert note_entity.content is not None
    assert note_entity.author_id is not None

    basic_args = drop_undefined(
        drop_except_keys(
            asdict(note_entity), 
            {"note_id", "title", "content", "author_id", "updated_at"}
        )
    )
    basic_args["id"] = basic_args.pop("note_id")
    basic_args["stripped_content"] = basic_args.pop("content")

    return MinimalNote(**basic_args)


def to_search_type(proto_value: GetSearchNotesRequest.SearchType.ValueType) ->  SearchType:
    if proto_value == GetSearchNotesRequest.SearchType.Undefined:
        return SearchType.CONTEXT
    elif proto_value == GetSearchNotesRequest.SearchType.NoSearch:
        return SearchType.NO_SEARCH
    elif proto_value == GetSearchNotesRequest.SearchType.FullTextTitle:
        return SearchType.FULL_TEXT_TITLE
    elif proto_value == GetSearchNotesRequest.SearchType.Fuzzy:
        return SearchType.FUZZY
    elif proto_value == GetSearchNotesRequest.SearchType.Context:
        return SearchType.CONTEXT
    else:
        raise ValueError(f"Unknown SearchType value: {proto_value}")

