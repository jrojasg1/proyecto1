import grpc
import requests
import sys
import os
import random
sys.path.append('../Proto/ServiceClient')
import Service_pb2
import Service_pb2_grpc

CHUNK_SIZE = 400

def write_file(file_path, file_id):
    try:
        with open(file_path, 'rb') as file:
            chunk_id = 0
            while True:
                datanode_info = get_datanode_address()
                print(datanode_info)
                if datanode_info:
                    datanode_address = datanode_info["address"]
                    print(f"DataNode seleccionado: Dirección {datanode_address}")
                else:
                    print("No se pudo obtener información del DataNode del servidor NameNode")
                    return False
                
                channel = grpc.insecure_channel(datanode_address)
                stub = Service_pb2_grpc.DatanodeServiceStub(channel)
                chunk_data = file.read(CHUNK_SIZE)
                if not chunk_data:
                    break
                request = Service_pb2.WriteRequest(file_id=file_id, chunk_id=chunk_id, data=chunk_data)
                response = stub.WriteData(request)
                if response.success:
                    print(f"Chunk {chunk_id} enviado con éxito al DataNode.")
                    send_chunk_path_to_namenode(datanode_address, file_id, chunk_id)
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

def send_chunk_path_to_namenode(datanode_address, file_id, chunk_id):
    try:
        response = requests.post('http://localhost:5000/chunk', json={'datanode_address': datanode_address, 'file_id': file_id, 'chunk_id': chunk_id})
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

def get_chunk_paths_from_namenode(file_id):
    try:
        response = requests.get(f'http://localhost:5000/chunk?file_id={file_id}')
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener las rutas de los chunks del NameNode.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud al NameNode:", e)
        return None
    
def read_chunk_from_datanode(datanode_address, file_id, chunk_id, size):
    try:
        channel = grpc.insecure_channel(datanode_address)
        stub = Service_pb2_grpc.DatanodeServiceStub(channel)
        read_request = Service_pb2.ReadRequest(
            file_id=file_id,
            chunk_id=chunk_id,
            size=size
        )

        response = stub.ReadData(read_request)
        if response.success:
            return response.data
        else:
            print(f"Failed to read chunk {chunk_id} from DataNode.")
            return None
    except grpc.RpcError as e:
        print(f"Error communicating with DataNode: {e}")
        return None

def main():
    print("1. Escribir archivo")
    print("2. Leer archivo")
    option = input("Seleccione una opción: ")

    if option == '1':
        # Pedir al usuario el file_path y file_id
        file_path = input("Ingrese la ruta del archivo: ")
        file_id = input("Ingrese el ID del archivo: ")
        write_success = write_file(file_path, file_id)
        if write_success:
            print("File successfully written to DataNode")
        else:
            print("Failed to write file to DataNode")

    elif option == '2':
        file_id = input("Ingrese el ID del archivo a leer: ")
        output_file_path = f"{file_id}_output_file"

        with open(output_file_path, "wb") as output_file:
            chunk_paths = get_chunk_paths_from_namenode(file_id)
            for chunk_path in chunk_paths:
                chunk_id = chunk_path["chunk_id"]
                datanode_address = chunk_path["datanode_address"]
                chunk_data = read_chunk_from_datanode(datanode_address, file_id, chunk_id, CHUNK_SIZE)
                if chunk_data:
                    output_file.write(chunk_data)
                    print(f"Chunk {chunk_id} written to output file.")
                else:
                    print(f"Failed to read chunk {chunk_id} from DataNode.")

        print("All chunks have been written to the output file:", output_file_path)

    else:
        print("Opción inválida.")

if __name__ == '__main__':
    main()
