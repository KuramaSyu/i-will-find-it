import asyncio
import grpc
from grpc_mod.proto.note_pb2_grpc import add_NoteServiceServicer_to_server
from grpc_mod.service import GRPCNoteService
from db.repos import NoteRepoABC, NotePostgreRepo


async def serve():
    # 1. Initialize your repository (async DB layer)
    repo: NoteRepoABC = NotePostgreRepo()  # replace with your actual async repo implementation

    # 2. Create your gRPC server
    server = grpc.aio.server()

    # 3. Register your service
    add_NoteServiceServicer_to_server(GRPCNoteService(repo), server)

    # 4. Listen on a port
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    print(f"gRPC server listening on {listen_addr}")

    # 5. Start the server
    await server.start()

    # 6. Wait forever (or until cancelled)
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())