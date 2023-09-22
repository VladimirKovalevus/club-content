import grpc
import grpc_pb2 as pb2
import grpc_pb2_grpc as grpc_pb2


class TransmissionServicer(grpc_pb2.TransmissionServicer):

  def TakeFileFromServer(self, request, context):
    return super().TakeFileFromServer(request, context)
  def SendFileToServer(self, request, context):
    return super().SendFileToServer(request, context)
  def DeleteFileOnServer(self, request, context):
    return super().DeleteFileOnServer(request, context)