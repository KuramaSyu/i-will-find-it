from grpc.aio import ServicerContext

from db.repos import NoteRepoABC
from db.entities import NoteEntity
from grpc_mod.proto.note_pb2 import GetNoteRequest, NoteEmbedding, NotePermission, PostNoteRequest, Note
from grpc_mod.proto.note_pb2_grpc import NoteService, NoteServiceServicer


class GRPCNoteService(NoteServiceServicer):
    """
    Implements the gRPC service defined in grpc/proto/note.proto
    """

    def __init__(self, repo: NoteRepoABC):
        self.repo = repo

    async def get_note(self, request: GetNoteRequest, ctx: ServicerContext) -> Note:
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

    async def post_note(self, request: PostNoteRequest, ctx: ServicerContext) -> Note:
        ...