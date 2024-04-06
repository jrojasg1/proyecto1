import requests
import grpc
import sys
sys.path.append('../Proto/ServiceClient')
import Service_pb2
import Service_pb2_grpc


CHUNK_SIZE = 1024

NAME_NODE_URL = 'http://localhost:5000/chunks'

def write_file(stub, file_path, file_id):
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

def divide_file(filename):
    chunks = []
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            chunks.append(chunk)
    return chunks

def send_num_chunks_to_namenode(filename, chunk_index, num_chunks):
    data = {
        "filename": filename,
        "chunk_index": chunk_index,
        "num_chunks": num_chunks
    }
    response = requests.post(NAME_NODE_URL, json=data)
    return response.json().get("datanode_id")
       
def main():
    datanode_info = get_datanode_address()
    if datanode_info:
        datanode_id = datanode_info["id"]
        datanode_address = datanode_info["address"]
        print(f"DataNode seleccionado: ID {datanode_id}, Dirección {datanode_address}")
        # Aquí podrías utilizar la información del DataNode para guardar los bloques
    else:
        print("No se pudo obtener información del DataNode del servidor NameNode")

    channel = grpc.insecure_channel(datanode_address)
    stub = Service_pb2_grpc.DatanodeServiceStub(channel)

    file_path = 'yo.txt'
    file_id = "example_file_2"
    write_success = write_file(stub, file_path, file_id)
    if write_success:
        print("File successfully written to datanode")
        data_read = read_file(stub, file_id, 0, 18)
        if data_read:
            with open("archivo_recibido.txt", "wb") as file:
                file.write(data_read)
            print("Archivo recibido desde el datanode y guardado como 'archivo_recibido.txt'.")
        else:
            print("Error al leer el archivo desde el datanode.")
    else:
        print("Failed to write file to datanode")

if __name__ == '__main__':
    main()
