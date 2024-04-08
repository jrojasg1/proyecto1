import grpc
import requests
import sys
sys.path.append('../Proto/ServiceClient')
import Service_pb2
import Service_pb2_grpc

CHUNK_SIZE = 400

def write_file(stub, datanode_address, file_path, file_id):
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
                    send_chunk_path_to_namenode(datanode_address,file_id, f"{file_id}_chunk_{chunk_id}")
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

def send_chunk_path_to_namenode(datanode_address,file_id, chunk_path):
    if datanode_address:
        response = requests.post('http://localhost:5000/chunk', json={'datanode_address': datanode_address, 'chunk_path': chunk_path})
        if response.status_code == 200:
            print("Ruta del chunk enviada al NameNode.")
        else:
            print("Error al enviar la ruta del chunk al NameNode.")
    else:
        print("No se pudo obtener información del DataNode del servidor NameNode")

def get_datanode_address():
    response = requests.get('http://localhost:5000/datanodes')
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def read_file(stub, file_id, datanode_address):
    if datanode_address:
        channel = grpc.insecure_channel(datanode_address)
        stub = Service_pb2_grpc.DatanodeServiceStub(channel)
        chunk_paths = get_chunk_paths(datanode_address, file_id)
        if chunk_paths:
            for chunk_path in chunk_paths:
                chunk_id = int(chunk_path.split("_chunk_")[1])
                response = read_chunk(stub, file_id, chunk_id) 
                if response:              
                    print(f"Data read from chunk: {response}")
                else:
                    print(f"Failed to read data from chunk: {chunk_id}")
        else:
            print("No chunk paths found for the file.")
    else:
        print("No se pudo obtener información del DataNode del servidor NameNode")

def get_chunk_paths(datanode_address, file_id):
    response = requests.get(f'http://localhost:5000/chunk?datanode_address={datanode_address}&file_id={file_id}')
    if response.status_code == 200:
        return response.json()["chunk_paths"]
    else:
        return None

def read_chunk(stub, file_id, chunk_path):
    request = Service_pb2.ReadRequest(file_id=file_id, chunk_path=chunk_path)
    response = stub.ReadData(request)
    return response.data if response.success else None

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
    write_success = write_file(stub, datanode_address, file_path, file_id)
    if write_success:
        print("File successfully written to DataNode")

    else:
        print("Failed to write file to DataNode")

    read_data = read_file(stub, file_id)

    if read_data:
        print(f'datos: {read_data}')

if __name__ == '__main__':
    main()
