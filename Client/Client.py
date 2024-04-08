import grpc
import requests
import sys
sys.path.append('../Proto/ServiceClient')
import Service_pb2
import Service_pb2_grpc

CHUNK_SIZE = 400


def write_file(stub, file_path, file_id):
    try:
        with open(file_path, 'rb') as file:
            chunk_id = 0
            while True:
                chunk_data = file.read(CHUNK_SIZE)
                if not chunk_data:
                    break
                request = Service_pb2.WriteRequest(file_id=file_id, chunk_id=chunk_id, data=chunk_data)
                response = stub.WriteData(request)
                if response.success:
                    print(f"Chunk {chunk_id} enviado con éxito al DataNode.")
                else:
                    print(f"Fallo al enviar el Chunk {chunk_id} al DataNode.")
                chunk_id += 1
            return True
    except FileNotFoundError:
        print("File not found:", file_path)
        return False
    except Exception as e:
        print("Error:", e)
        return False

def read_file(stub, file_id, offset, size):
    request = Service_pb2.ReadRequest(file_id=file_id, offset=offset, size=size)
    response = stub.ReadData(request)
    return response.data if response.success else None

def get_datanode_address():
    response = requests.get('http://localhost:5000/datanodes')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    # Get DataNode address from NameNode
    datanode_info = get_datanode_address()
    print('datanode_info: ', datanode_info )
    if datanode_info:
        datanode_id = datanode_info["id"]
        datanode_address = datanode_info["address"]
        print(f"DataNode seleccionado: ID {datanode_id}, Dirección {datanode_address}")
    else:
        print("No se pudo obtener información del DataNode del servidor NameNode")
        return

    # Connect to DataNode
    channel = grpc.insecure_channel(datanode_address)
    stub = Service_pb2_grpc.DatanodeServiceStub(channel)

    # Define file path and ID
    file_path = 'yo.txt'
    file_id = "example_file_2"

    # Write file to DataNode
    write_success = write_file(stub, file_path, file_id)
    if write_success:
        print("File successfully written to DataNode")

        # Read file from DataNode
        '''data_read = read_file(stub, file_id, 0, 18)
        if data_read:
            with open("archivo_recibido.txt", "wb") as file:
                file.write(data_read)
            print("Archivo recibido desde el DataNode y guardado como 'archivo_recibido.txt'.")
        else:
            print("Error al leer el archivo desde el DataNode.")
        '''
    else:
        print("Failed to write file to DataNode")

if __name__ == '__main__':
    main()
