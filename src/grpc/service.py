from grpc.aio import ServicerContext

from db.repos import NoteRepoABC
from db.entities import NoteEntity
from grpc.generated import PostNoteRequest, GetNoteRequest, NoteServiceServicer, Note


class GRPCNoteService(NoteServiceServicer):
    """
    Implements the gRPC service defined in grpc/proto/note.proto
    """

    def __init__(self, repo: NoteRepoABC):
        self.repo = repo

    async def get_note(self, request: GetNoteRequest, ctx: ServicerContext) -> Note:
        await self.repo.select(note=NoteEntity(
            note_id=request.id,
            author_id=None,
            content=None,
            embeddings=None,
            permissions=None,
            title=None,
            updated_at=None
        ))

    async def post_note(self, request: PostNoteRequest, ctx: ServicerContext) -> Note:
        ...