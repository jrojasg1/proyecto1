from flask import Flask, request
import requests
import shutil
import threading
import time
from concurrent import futures 
import grpc
import sys
import os
sys.path.append('../../Proto/ServiceClient')
import Service_pb2
import Service_pb2_grpc

app = Flask(__name__)

DATANODE_ID = 1
IP_ADDRESS = 'localhost'
PORT = 50051
PORT_REST = 20051
NAMENODE_ADDRESS = 'localhost:5000'

class DataNode:
    def __init__(self, datanode_id, datanode_ip_address, datanode_port, datanode_port_rest, namenode_address):
        self.datanode_id = datanode_id
        self.datanode_ip_address = datanode_ip_address
        self.datanode_port = datanode_port
        self.storage_path = os.path.join(os.getcwd())
        self.namenode_address = namenode_address
        self.datanode_port_rest = datanode_port_rest

        # Iniciar el envío periódico del latido del nodo de datos
        heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

    def send_heartbeat(self):
        capacity = self.get_capacity()
        
        while True:
            try:
                print('capacidad: ', capacity)
                response = requests.post(f'http://{self.namenode_address}/heartbeat', json={
                    'id': self.datanode_id,
                    'address': self.datanode_ip_address + ':' + str(self.datanode_port),
                    'address_rest': self.datanode_ip_address + ':' + str(self.datanode_port_rest),
                    'capacity': capacity,
                    'rack': 1
                })
                if response.status_code == 200:
                    print("Heartbeat sent to NameNode.")
                else:
                    print("Error sending heartbeat to NameNode.")
            except requests.exceptions.RequestException as e:
                print(f"Connection error: {e}")
            time.sleep(10)

    def get_capacity(self):
        total, used, free = shutil.disk_usage(self.storage_path)
        return free  

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Service_pb2_grpc.add_DatanodeServiceServicer_to_server(self, server)
        server.add_insecure_port('[::]:'+ str(PORT))
        server.start()
        server.wait_for_termination()

    def WriteData(self, request, context):
        file_id = request.file_id
        chunk_id = request.chunk_id
        data = request.data
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        chunk_path = os.path.join(self.storage_path, f"{file_id}_chunk_{chunk_id}")
        with open(chunk_path, 'wb') as f:
            f.write(data)
        response = Service_pb2.WriteResponse(success=True)
        print(f"Chunk {chunk_id} saved at {chunk_path}")
        
        return response

    def ReadData(self, request, context):
        file_id = request.file_id
        chunk_id = request.chunk_id
        chunk_path = os.path.join(self.storage_path, f"{file_id}_chunk_{chunk_id}")
        if os.path.exists(chunk_path):
            with open(chunk_path, 'rb') as f:
                data = f.read()
                response = Service_pb2.ReadResponse(data=data, success=True)
                print(f"Chunk {chunk_id} sent to client")
        else:
            response = Service_pb2.ReadResponse(success=False)
            print(f"Chunk {chunk_id} not found")
        return response

    @app.route('/ping', methods=['GET'])
    def ping_datanode():
        return 'Pong'

    def run_rest_server(self):
        app.run(host=self.datanode_ip_address, port=self.datanode_port_rest)

if __name__ == '__main__':
    datanode_id = DATANODE_ID
    datanode_ip_address = IP_ADDRESS
    datanode_port = PORT
    datanode_port_rest = PORT_REST
    namenode_address = NAMENODE_ADDRESS

    data_node = DataNode(datanode_id, datanode_ip_address, datanode_port, datanode_port_rest, namenode_address)
    rest_thread = threading.Thread(target=data_node.run_rest_server)

    rest_thread.start()
    data_node.serve()
