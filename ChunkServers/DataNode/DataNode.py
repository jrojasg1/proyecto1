import json
import grpc
from concurrent import futures
import sys
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
    def __init__(self, data_node_id, address):
        self.data_node_id = data_node_id
        self.address = address
        self.data_store = {}

    def WriteData(self, request, context):
        print("Received WriteRequest:", request)
        file_id = request.file_id
        data = request.data
        self.data_store[file_id] = data
        response = Service_pb2.WriteResponse(success=True)
        print("Sending WriteResponse:", response)
        print("Data Store:", self.data_store)
        return response

    def ReadData(self, request, context):
        print("Received ReadRequest:", request)
        file_id = request.file_id
        if file_id in self.data_store:
            data = self.data_store[file_id]
            response = Service_pb2.ReadResponse(data=data, success=True)
        else:
            response = Service_pb2.ReadResponse(success=False)
        print("Sending ReadResponse:", response)
        return response

    def ReceiveData(self, data):
        # Método para recibir datos de otros DataNodes
        print(f"Data received at {self.address}: {data}")
        return True

def load_datanodes_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    datanodes = {}
    for datanode_info in config["datanodes"]:
        data_node_id = datanode_info["id"]
        address = datanode_info["address"]
        datanodes[address] = DataNode(data_node_id, address)
    return datanodes

def serve():
    data_nodes = load_datanodes_config("DataNodes.json")
    chunk_server = ChunkServer(data_nodes)
    chunk_server.serve(50052)

if __name__ == '__main__':
    serve()