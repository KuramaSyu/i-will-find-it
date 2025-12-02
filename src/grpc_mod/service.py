from datetime import datetime

from grpc.aio import ServicerContext

from db.repos import NoteRepoABC
from db.entities import NoteEntity
from grpc_mod import (
    GetNoteRequest, NoteEmbedding, 
    NotePermission, PostNoteRequest, Note,
    NoteService, NoteServiceServicer,
    UserServiceServicer, GetUserRequest, User, 
    AlterUserRequest, DeleteUserRequest, 
    DeleteUserResponse, PostUserRequest
)
from grpc_mod.converter import to_grpc_note
from db.repos.user.user import UserRepositoryABC


class GRPCNoteService(NoteServiceServicer):
    """
    Implements the gRPC service defined in grpc/proto/note.proto
    """

    def __init__(self, repo: NoteRepoABC):
        self.repo = repo

    async def GetNote(self, request: GetNoteRequest, context: ServicerContext) -> Note:
        note_entity = await self.repo.select(note=NoteEntity(
            note_id=request.id,
            author_id=None,
            content=None,
            embeddings=[],
            permissions=[],
            title=None,
            updated_at=None
        ))
        assert (note_entity.note_id 
            and note_entity.author_id 
            and note_entity.content 
            and note_entity.title
        )

        # conversion from note_entity to gRPC Note Message
        return Note(
            id=note_entity.note_id,
            title=note_entity.title,
            author_id=note_entity.author_id,
            content=note_entity.content,
            embeddings=[
                NoteEmbedding(
                    model=e.model,
                    embedding=e.embedding,
                ) for e in note_entity.embeddings
            ],
            permissions=[
                NotePermission(
                    role_id=p.role_id
                ) for p in note_entity.permissions
            ]

        )

    async def PostNote(self, request: PostNoteRequest, context: ServicerContext) -> Note:
        note_entity = await self.repo.insert(
            NoteEntity(
                note_id=None,
                author_id=request.author_id,
                content=request.content.value,
                embeddings=[],
                permissions=[],
                title=request.title.value,
                updated_at=datetime.now(),
            )
        )
        return to_grpc_note(note_entity)

class GRPCUserService(UserServiceServicer):
    """
    Implements the gRPC service defined in grpc/proto/user.proto
    """

    def __init__(self, user_repo: UserRepositoryABC):
        self.repo = user_repo

    async def GetUser(self, request: GetUserRequest, context: ServicerContext) -> User:
        ...

    async def AlterUser(self, request: AlterUserRequest, context: ServicerContext) -> User:
        ...
    
    async def DeleteUser(self, request: DeleteUserRequest, context: ServicerContext) -> DeleteUserResponse:
        ...
    
    async def PostUser(self, request: PostUserRequest, context: ServicerContext) -> User:
        ...
