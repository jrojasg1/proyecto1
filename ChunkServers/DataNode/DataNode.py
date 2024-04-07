import grpc
from concurrent import futures
import sys
import os
sys.path.append('../../Proto/ServiceClient')
import Service_pb2
import Service_pb2_grpc

class ChunkServer(Service_pb2_grpc.ChunkServerServiceServicer):
    def __init__(self, data_nodes):
        self.data_nodes = data_nodes

    def SendData(self, request, context):
        destination_address = request.destination_address
        data = request.data
        success = False

        if destination_address in self.data_nodes:
            data_node = self.data_nodes[destination_address]
            success = data_node.ReceiveData(data)

        return Service_pb2.SendDataResponse(success=success)

    def serve(self, port):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Service_pb2_grpc.add_ChunkServerServiceServicer_to_server(self, server)
        server.add_insecure_port('[::]:' + str(port))
        server.start()
        server.wait_for_termination()

class DataNode(Service_pb2_grpc.DatanodeServiceServicer):
    def __init__(self, data_node_id, chunk_id, address,storage_path):
        self.data_node_id = data_node_id
        self.chunk_id = chunk_id  # Se añade el identificador del chunk
        self.address = address
        self.storage_path = storage_path
        self.data_store = {}

    def WriteData(self, request, context):
        print("Received WriteRequest:", request)
        file_id = request.file_id
        data = request.data
        
        # Guardar el archivo en el sistema de archivos local
        file_path = os.path.join(self.storage_path, f"{file_id}")
        with open(file_path, 'wb') as f:
            f.write(data)
        
        response = Service_pb2.WriteResponse(success=True)
        print("Sending WriteResponse:", response)
        return response

    def ReadData(self, request, context):
        print("Received ReadRequest:", request)
        file_id = request.file_id
        print("data store:", self.data_store)
        if file_id in self.data_store:
            data = self.data_store[file_id]
            response = Service_pb2.ReadResponse(data=data, success=True)
        else:
            response = Service_pb2.ReadResponse(success=False)
        print("Sending ReadResponse:", response)
        return response

    def ReceiveData(self, data):
        # Método para recibir datos de otros DataNodes
        print(f"Data received at {self.address} (Chunk {self.chunk_id}): {data}")
        return True

def load_datanodes_config(name_node_address):
    channel = grpc.insecure_channel(name_node_address)
    stub = Service_pb2_grpc.NameNodeServiceStub(channel)
    response = stub.GetDatanodesConfig(Service_pb2.Empty())
    
    datanodes = {}
    for chunk_info in response.datanodes:
        for datanode_info in chunk_info.datanodes:
            data_node_id = datanode_info.id
            address = datanode_info.address
            chunk_id = chunk_info.id
            datanodes[address] = DataNode(data_node_id, chunk_id, address)
    return datanodes

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Service_pb2_grpc.add_DatanodeServiceServicer_to_server(DataNode(1,'localhost','../DataNode'), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
