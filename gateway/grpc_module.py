import grpc
import grpc_helper
import grpc_pb2 as pb2
import grpc_pb2_grpc as grpc_pb2

gRPC_ADRS = 'localhost:8785'

def CreateUser(login: str, password: str, workspace_id: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.User(login=login, password=password, workspace_id=workspace_id)
        responce = stub.CreateUser(req)
    return responce

def UpdateUser(login: str, password: str, workspace_id: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.User(login=login, password=password, workspace_id=workspace_id)
        responce = stub.UpdateUser(req)
    return responce

def ReadUser(login: str, password: str, workspace_id: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.User(login=login, password=password, workspace_id=workspace_id)
        responce = stub.ReadUser(req)
    return responce

###

def CreateWorkspace(name: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.Workspace(name=name)
        responce = stub.CreateWorkspace(req)
    return responce

###

def CreateFile(workspace_id: str, path: str, buffer: bytes):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.File(workspace_id=workspace_id, path=path, buffer=buffer)
        responce = stub.CreateFile(req)
    return responce

def GetFile(workspace_id: str, path: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.WorkspaceFile(workspace_id=workspace_id, path=path)
        responce = stub.GetFile(req)
    return responce

def DeleteFile(path: str, workspace_id: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.File(path=path, workspace_id=workspace_id)
        responce = stub.DeleteFile(req)
    return responce

###

def CreateFolder(path: str, workspace_id: str, skip=int, take=int):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.Folder(path=path, workspace_id=workspace_id, skip=skip, take=take)
        responce = stub.CreateFolder(req)
    return responce

def GetFolder(path: str, workspace_id: str, skip=int, take=int):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.Folder(path=path, workspace_id=workspace_id, skip=skip, take=take)
        responce = stub.GetFolder(req)
    return responce

def DeleteFolder(path: str, workspace_id: str, skip=int, take=int):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.Folder(path=path, workspace_id=workspace_id, skip=skip, take=take)
        responce = stub.DeleteFolder(req)
    return responce



