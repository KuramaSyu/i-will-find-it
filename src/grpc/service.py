from grpc.aio import ServicerContext

from generated import NoteService, NoteServiceServicer, NoteServiceStub, GetNoteRequest, Note, PostNoteRequest
from db.repos import NoteRepoABC


class GRPCNoteService(NoteServiceServicer):
    """
    Implements the gRPC service defined in grpc/proto/note.proto
    """

    def __init__(self, repo: NoteRepoABC):
        self.repo = repo

    async def get_note(self, request: GetNoteRequest, ctx: ServicerContext) -> Note:
        ...

    async def post_note(self, request: PostNoteRequest, ctx: ServicerContext) -> Note:
        ...