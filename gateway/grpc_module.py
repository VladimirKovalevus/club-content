import grpc
import grpc_pb2 as pb2
import grpc_pb2_grpc as grpc_pb2
from google.protobuf.json_format import Parse, ParseDict, MessageToDict
import json

gRPC_ADRS = 'localhost:8785'

def CreateUser(login: str, password: str, workspace_id: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.User(login=login, password=password, workspace_id=workspace_id)
        responce = stub.CreateUser(req)
        message = MessageToDict(responce)
    return message

def UpdateUser(login: str, password: str, workspace_id: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.User(login=login, password=password, workspace_id=workspace_id)
        responce = stub.UpdateUser(req)
        message = MessageToDict(responce)
    return message

def ReadUser(login: str, password: str, workspace_id: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.User(login=login, password=password, workspace_id=workspace_id)
        responce = stub.ReadUser(req)
        message = MessageToDict(responce)
    return message

###

def CreateWorkspace(name: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.Workspace(name=name)
        responce = stub.CreateWorkspace(req)
        message = MessageToDict(responce)
    return message

###

def CreateFile(workspace_id: str, path: str, buffer: bytes):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.File(workspace_id=workspace_id, path=path, buffer=buffer)
        responce = stub.CreateFile(req)
        message = MessageToDict(responce)
    return message

def GetFile(workspace_id: str, path: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.WorkspaceFile(workspace_id=workspace_id, path=path)
        responce = stub.GetFile(req)
        message = MessageToDict(responce)
    return message

def DeleteFile(path: str, workspace_id: str):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.File(path=path, workspace_id=workspace_id)
        responce = stub.DeleteFile(req)
        message = MessageToDict(responce)
    return message

###

def CreateFolder(path: str, workspace_id: str, skip=int, take=int):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.Folder(path=path, workspace_id=workspace_id, skip=skip, take=take)
        responce = stub.CreateFolder(req)
        message = MessageToDict(responce)
    return message

def GetFolder(path: str, workspace_id: str, skip=int, take=int):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.Folder(path=path, workspace_id=workspace_id, skip=skip, take=take)
        responce = stub.GetFolder(req)
        message = MessageToDict(responce)
    return message

def DeleteFolder(path: str, workspace_id: str, skip=int, take=int):
    with grpc.insecure_channel(gRPC_ADRS) as channel:
        stub = grpc_pb2.TransmissionStub(channel)
        req = pb2.Folder(path=path, workspace_id=workspace_id, skip=skip, take=take)
        responce = stub.DeleteFolder(req)
        message = MessageToDict(responce)
    return message



