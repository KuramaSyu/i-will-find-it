import grpc
from grpc_mod import NoteService
from google.protobuf.wrappers_pb2 import Int32Value, StringValue

def get_note(stub, note_id):
    request = note_pb2.GetNoteRequest(id=note_id)
    response = stub.GetNote(request)
    print("GetNote response:")
    print(response)
    return response

def post_note(stub, note_id=None, title=None, content=None, author_id=1):
    request = note_pb2.PostNoteRequest(
        id=Int32Value(value=note_id) if note_id is not None else None,
        title=StringValue(value=title) if title is not None else None,
        content=StringValue(value=content) if content is not None else None,
        author_id=author_id,
    )

    response = stub.PostNote(request)
    print("PostNote response:")
    print(response)
    return response

def main():
    # Connect to server
    channel = grpc.insecure_channel("localhost:50051")
    stub = note_pb2_grpc.NoteServiceStub(channel)

    # Test: create/update note
    print("Posting note...")
    post_note(
        stub,
        note_id=None,           # None → create new
        title="Hello World",
        content="This is a test note",
        author_id=123
    )

    # Test: fetch note
    print("\nFetching note...")
    get_note(stub, note_id=1)

if __name__ == "__main__":
    main()
