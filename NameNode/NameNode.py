import grpc
import json
import sys
sys.path.append('../../Proto/ServiceNameNode')
import NameNodeService_pb2
import NameNodeService_pb2_grpc

class NameNode(NameNodeService_pb2_grpc.NameNodeServiceServicer):
    def __init__(self, config_file):
        self.config_file = config_file

    def GetDatanodesConfig(self, request, context):
        with open(self.config_file) as f:
            config = json.load(f)

        datanodes_config = NameNodeService_pb2.DatanodesConfig()
        for chunk_info in config["chunkservers"]:
            for datanode_info in chunk_info["datanodes"]:
                datanode = datanodes_config.datanodes.add()
                datanode.id = datanode_info["id"]
                datanode.address = datanode_info["address"]
                datanode.chunk_id = chunk_info["id"]  # Se añade el identificador del chunk

        return datanodes_config

def serve():
    server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
    NameNodeService_pb2_grpc.add_NameNodeServiceServicer_to_server(NameNode("DataNodes.json"), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
