# i-will-find-it

# Todo
- UserRepo
- gRPC user service

# Development Docs
### Compile Protobufs (`.proto` files):
1. install requirements:
    ```bash
    pip install -r requirements.txt
    ```
2. [install protobuf compiler on the system](https://github.com/protocolbuffers/protobuf#protobuf-compiler-installation)
3. compile the `src/grpc_mod/note.proto` and `src/grpc_mod/user.proto`file:
    ```bash
    python -m grpc_tools.protoc \
            -I. \
            --python_out=. \
            --grpc_python_out=. \
            --mypy_out=. \
            grpc_mod/proto/*.proto
    ```

### Start gRPC server
```bash
cd src
env PYTHONTRACEMALLOC=1 python main.py
```