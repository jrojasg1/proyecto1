import grpc
import requests
import sys
import os
sys.path.append('../Proto/ServiceClient')
import Service_pb2
import Service_pb2_grpc

CHUNK_SIZE = 400

def write_file(datanode_address, file_path, file_id):
    try:
        channel = grpc.insecure_channel(datanode_address)
        stub = Service_pb2_grpc.DatanodeServiceStub(channel)
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
                    send_chunk_path_to_namenode(datanode_address, file_id, f"{file_id}_chunk_{chunk_id}")
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

def send_chunk_path_to_namenode(datanode_address, file_id, chunk_path):
    try:
        response = requests.post('http://localhost:5000/chunk', json={'datanode_address': datanode_address, 'file_id': file_id, 'chunk_path': chunk_path})
        if response.status_code == 200:
            print("Ruta del chunk enviada al NameNode.")
        else:
            print("Error al enviar la ruta del chunk al NameNode.")
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud al NameNode:", e)

def get_datanode_address():
    response = requests.get('http://localhost:5000/datanodes')
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def read_chunk_from_datanode(datanode_address, file_id, chunk_id, size):
    try:
        # Conectar al DataNode
        channel = grpc.insecure_channel(datanode_address)
        stub = Service_pb2_grpc.DatanodeServiceStub(channel)

        # Crear la solicitud de lectura
        read_request = Service_pb2.ReadRequest(
            file_id=file_id,
            chunk_id=chunk_id,
            size=size
        )

        # Enviar la solicitud de lectura al DataNode
        response = stub.ReadData(read_request)

        # Verificar si la solicitud fue exitosa y devolver los datos del chunk
        if response.success:
            return response.data
        else:
            print(f"Failed to read chunk {chunk_id} from DataNode.")
            return None
    except grpc.RpcError as e:
        print(f"Error communicating with DataNode: {e}")
        return None

def get_chunk_paths_from_namenode(datanode_address, file_id):
    if datanode_address:
        response = requests.get(f'http://localhost:5000/chunk?file_id={file_id}')
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener las rutas de los chunks del NameNode.")
            return None
    else:
        print("No se pudo obtener información del DataNode del servidor NameNode")
        return None
    
def main():
    print("1. Escribir archivo")
    print("2. Leer archivo")
    option = input("Seleccione una opción: ")

    if option == '1':
        # Get DataNode address from NameNode
        datanode_info = get_datanode_address()
        print('datanode_info: ', datanode_info)
        if datanode_info:
            datanode_id = datanode_info["id"]
            datanode_address = datanode_info["address"]
            print(f"DataNode seleccionado: ID {datanode_id}, Dirección {datanode_address}")
        else:
            print("No se pudo obtener información del DataNode del servidor NameNode")
            return
        # Pedir al usuario el file_path y file_id
        file_path = input("Ingrese la ruta del archivo: ")
        file_id = input("Ingrese el ID del archivo: ")
        write_success = write_file(datanode_address, file_path, file_id)
        if write_success:
            print("File successfully written to DataNode")
            
        else:
            print("Failed to write file to DataNode")

    elif option == '2':
        # Pedir al usuario el file_id
        file_id = input("Ingrese el ID del archivo a leer: ")
        # Get DataNode address from NameNode
        datanode_info = get_datanode_address()
        print('datanode_info: ', datanode_info)
        if datanode_info:
            datanode_id = datanode_info["id"]
            datanode_address = datanode_info["address"]
            print(f"DataNode seleccionado: ID {datanode_id}, Dirección {datanode_address}")
        else:
            print("No se pudo obtener información del DataNode del servidor NameNode")
            return
        chunk_id = 0  # ID del chunk
        size = CHUNK_SIZE  # Tamaño de los datos a leer

        # Llamar a la función para leer el chunk del DataNode
        chunk_data = read_chunk_from_datanode(datanode_address, file_id, chunk_id, size)

        if chunk_data:
            print("Chunk data:", chunk_data)
        else:
            print("Failed to read chunk from DataNode.")

    else:
        print("Opción inválida.")

if __name__ == '__main__':
    main()
