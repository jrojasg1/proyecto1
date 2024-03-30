import grpc
from concurrent import futures
import sys
sys.path.append('../../Proto')  # Agrega la ruta al directorio que contiene el módulo generado
import Service_pb2
import Service_pb2_grpc

class Datanode(Service_pb2_grpc.DatanodeServiceServicer):
    def __init__(self):
        self.data_store = {}

    def WriteData(self, request, context):
        print("Received WriteRequest:", request)
        file_id = request.file_id
        data = request.data
        self.data_store[file_id] = data
        response = Service_pb2.WriteResponse(success = 1)
        print("Sending WriteResponse:", response)
        return response

    def ReadData(self, request, context):
        print("Received ReadRequest:", request)
        file_id = request.file_id
        if file_id in self.data_store:
            data = self.data_store[file_id]
            response =  Service_pb2.ReadResponse(data=data, success=1)
        else:
            response =  Service_pb2.ReadResponse(success=False)
        print("Sending ReadResponse:", response)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Service_pb2_grpc.add_DatanodeServiceServicer_to_server(Datanode(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    