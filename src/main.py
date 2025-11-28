import asyncio
import grpc
from grpc_mod import add_NoteServiceServicer_to_server, GRPCNoteService
from db.repos import NoteRepoABC, NotePostgreRepo
from db import Database


async def serve():
    db = Database(dsn="postgres://postgres:postgres@localhost:5433/db?sslmode=disable")
    await db.init_db()
    repo: NoteRepoABC = NotePostgreRepo(db=db)
    note_service = GRPCNoteService(repo=repo)

    server = grpc.aio.server()
    add_NoteServiceServicer_to_server(note_service, server)

    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    print(f"gRPC server listening on {listen_addr}")

    # Start the server
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())