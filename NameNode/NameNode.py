import grpc
import json
import threading
from flask import Flask, jsonify, request
import sys
sys.path.append('../../Proto/ServiceNameNode')
import NameNodeService_pb2
import NameNodeService_pb2_grpc

app = Flask(__name__)

class NameNode(NameNodeService_pb2_grpc.NameNodeServiceServicer):
    def __init__(self, config_file):
        self.config_file = config_file

    def GetDatanodesConfig(self):
        with open(self.config_file) as f:
            config = json.load(f)
        datanodes_config = NameNodeService_pb2.DatanodesConfig()
        for chunk_info in config["chunkservers"]:
            for datanode_info in chunk_info["datanodes"]:
                datanode = datanodes_config.datanodes.add()
                datanode.id = datanode_info["id"]
                datanode.address = datanode_info["address"]
                datanode.chunk_id = chunk_info["id"]
        return datanodes_config

@app.route('/datanodes', methods=['GET'])
def get_datanodes_config():
    namenode = NameNode("DataNodes.json")
    datanodes_config = namenode.GetDatanodesConfig()
    return jsonify(datanodes_config.SerializeToString())

@app.route('/num_chunks', methods=['POST'])
def handle_num_chunks():
    data = request.json
    filename = data.get('filename')
    chunk_index = data.get('chunk_index')
    num_chunks = data.get('num_chunks')

    # Aquí iría la lógica para guardar el chunk en el DataNode
    datanode_id = 1

    return jsonify({'datanode_id': datanode_id})

def serve_grpc():
    server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
    NameNodeService_pb2_grpc.add_NameNodeServiceServicer_to_server(NameNode("DataNodes.json"), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    # Inicia el servidor gRPC en un hilo
    grpc_thread = threading.Thread(target=serve_grpc)
    grpc_thread.start()

    app.run(debug=True)
