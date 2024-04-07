import requests
import grpc
import sys
sys.path.append('../Proto/ServiceClient')
import Service_pb2
import Service_pb2_grpc

class Client:
    def __init__(self):
        self.CHUNK_SIZE = 1024
        self.NAME_NODE_URL = 'http://localhost:5000/chunks'

    def write_file(self, stub, file_path, file_id):
        """Escribe un archivo en el DataNode."""
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
                request = Service_pb2.WriteRequest(file_id=file_id, data=data)
                response = stub.WriteData(request)
                return response.success
        except FileNotFoundError:
            print("File not found:", file_path)
            return False
        except Exception as e:
            print("Error:", e)
            return False

    def read_file(self, stub, file_id, offset, size):
        """Lee un archivo desde el DataNode."""
        request = Service_pb2.ReadRequest(file_id=file_id, offset=offset, size=size)
        response = stub.ReadData(request)
        return response.data if response.success else None

    def get_datanode_address(self):
        """Obtiene la dirección del DataNode desde el servidor NameNode."""
        response = requests.get('http://localhost:5000/datanodes')
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def main(self):
        datanode_info = self.get_datanode_address()
        if datanode_info:
            datanode_id = datanode_info["id"]
            datanode_address = datanode_info["address"]
            print(f"DataNode seleccionado: ID {datanode_id}, Dirección {datanode_address}")
        else:
            print("No se pudo obtener información del DataNode del servidor NameNode")
            return

        # Establece la conexión gRPC con el DataNode
        channel = grpc.insecure_channel(datanode_address)
        stub = Service_pb2_grpc.DatanodeServiceStub(channel)

        # Escribe un archivo en el DataNode
        file_path = 'yo.txt'
        file_id = "example_file_2"
        if self.write_file(stub, file_path, file_id):
            print("File successfully written to datanode")
            
            # Lee el archivo desde el DataNode
            data_read = self.read_file(stub, file_id, 0, 18)
            if data_read:
                with open("archivo_recibido.txt", "wb") as file:
                    file.write(data_read)
                print("Archivo recibido desde el datanode y guardado como 'archivo_recibido.txt'.")
            else:
                print("Error al leer el archivo desde el datanode.")
        else:
            print("Failed to write file to datanode")

if __name__ == '__main__':
    client = Client()
    client.main()
