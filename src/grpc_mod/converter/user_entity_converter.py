from google.protobuf.timestamp_pb2 import Timestamp

from src.db.entities.note.metadata import NoteEntity
from src.grpc_mod.proto.note_pb2 import Note, NoteEmbedding, NotePermission
from src.grpc_mod import User
from src.db.entities.user.user import UserEntity

def to_grpc_user(user_entity: UserEntity) -> User:
    """Converts a UserEntity to a gRPC User message."""
    assert user_entity.id is not None
    assert user_entity.discord_id is not None
    assert user_entity.avatar_url is not None

    return User(
        id=user_entity.id,
        discord_id=user_entity.discord_id,
        avatar_url=user_entity.avatar_url,
    )




