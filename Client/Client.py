import grpc
import sys
sys.path.append('../Proto')  # Agrega la ruta al directorio que contiene el módulo generado
import Service_pb2
import Service_pb2_grpc

def write_data(stub, file_id, data):
    request = Service_pb2.WriteRequest(file_id=file_id, data=data)
    response = stub.WriteData(request)
    return response.success

def read_data(stub, file_id, offset, size):
    request = Service_pb2.ReadRequest(file_id=file_id, offset=offset, size=size)
    response = stub.ReadData(request)
    return response.data if response.success else None

def main():
    # Conexión al datanode
    channel = grpc.insecure_channel('localhost:50051')
    stub = Service_pb2_grpc.DatanodeServiceStub(channel)

    # Ejemplo de escritura y lectura de datos
    file_id = "example_file"
    data_to_write = b"Hello, world!"
    write_success = write_data(stub, file_id, data_to_write)
    if write_success:
        data_read = read_data(stub, file_id, 0, len(data_to_write))
        print("Data read:", data_read.decode() if data_read else "Failed to read data")
    else:
        print("Failed to write data")

if __name__ == '__main__':
    main()
