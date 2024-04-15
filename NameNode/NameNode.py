import threading
import time
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


datanodes_info = {}
datanodes_info_replicated = {}
chunk_paths = {}
max_inactive_time = 10

@app.route('/datanodes', methods=['GET'])
def get_datanode_info():
    try:
        response = requests.get('http://localhost:5000/ping')
        print(f'paths:  {datanodes_info}')
        if response.status_code == 200:
            datanode = response.json()
            datanode_fastest = datanode['fastest_datanode']
            print(response.json())
            
            if datanode_fastest:
                selected_datanode_info = datanodes_info.get(datanode_fastest)
                if selected_datanode_info and selected_datanode_info['capacity'] >= 400:
                    return jsonify(selected_datanode_info)
                else:
                    max_capacity_datanode = max(datanodes_info.values(), key=lambda x: x['capacity'])
                    return jsonify(max_capacity_datanode)
            else:
                return jsonify({"error": "No se encontró un DataNode disponible"}), 404
        else:
            return jsonify({"error": "Error al obtener la información del DataNode más rápido"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al obtener información del DataNode más rápido: {e}"}), 500
    
# Endpoint para recibir la información de un DataNode y almacenarla en el NameNode
@app.route('/heartbeat', methods=['POST'])
def register_datanode():
    data = request.json
    
    datanode_id = data.get('id')
    datanode_address = data.get('address')
    datanode_capacity = data.get('capacity')
    datanode_rack = data.get('rack')
    datanode_address_rest = data.get('address_rest')
    datanode_master = data.get('master')
    last_heartbeat = time.time()  # Marca de tiempo del último heartbeat
    
    if datanode_rack == 1:
        datanodes_info[datanode_id] = {
            'id': datanode_id,
            'address': datanode_address,
            'address_rest': datanode_address_rest,
            'capacity': datanode_capacity,
            'rack': datanode_rack,
            'last_heartbeat': last_heartbeat,
            'status': 'active'
        }
    else:
        datanodes_info_replicated[datanode_id] = {
            'id': datanode_id,
            'address': datanode_address,
            'address_rest': datanode_address_rest,
            'capacity': datanode_capacity,
            'rack': datanode_rack,
            'master': datanode_master,
            'last_heartbeat': last_heartbeat,
            'status': 'active'
        }

    return jsonify({'message': 'DataNode registrado exitosamente'})

# Endpoint para recibir la ruta de un chunk y almacenarla en el NameNode
@app.route('/chunk', methods=['POST'])
def register_chunk_path():
    data = request.json
    
    datanode_address = data.get('datanode_address')
    file_id = data.get('file_id')
    chunk_id = data.get('chunk_id')
    chunk_info = {
        'datanode_address':datanode_address,
        'chunk_id':chunk_id
    }
    if file_id in chunk_paths:
        chunk_paths[file_id].append(chunk_info)
    else:
        chunk_paths[file_id] = [chunk_info]
    print('chunk_paths: ', chunk_paths)
    return jsonify({'message': 'Ruta del chunk almacenada exitosamente'})

@app.route('/chunk', methods=['GET'])
def get_chunk_paths():
    file_id = request.args.get('file_id')
    
    if file_id:
        if file_id in chunk_paths:
            return jsonify(chunk_paths[file_id])
        else:
            return jsonify({"error": f"No se encontraron chunks para el archivo con ID {file_id}"}), 404
    else:
        return jsonify({"error": "Se requiere el parámetro 'file_id'"}), 400
    
# Endpoint para hacer ping al DataNode y medir el tiempo de respuesta
@app.route('/ping', methods=['GET'])
def ping_datanode():
    try:
        min_ping_time = float('inf')  # Inicializar el tiempo de ping mínimo como infinito
        fastest_datanode = None  # Inicializar el datanode más rápido como None
        
        for datanode_id, datanode_info in datanodes_info.items():
            if datanode_info['status'] == 'active':
          
                datanode_address = datanode_info['address_rest']
                start_time = time.time()
                response = requests.get(f'http://{datanode_address}/ping')
                
                if response.status_code == 200:
                    end_time = time.time()
                    ping_time = end_time - start_time
                    print(f'datanode {datanode_address} ping: {ping_time}')
                    if ping_time < min_ping_time:
                        min_ping_time = ping_time
                        fastest_datanode = datanode_id
        if fastest_datanode:
            return jsonify({'fastest_datanode': fastest_datanode, 'ping_time': min_ping_time})
        else:
            return jsonify({"error": "No se pudo establecer conexión con ningún DataNode"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al hacer ping a los DataNodes: {e}"}), 500


def check_datanode_status():
    # Función para verificar el estado de los DataNodes
    while True:
        current_time = time.time()
        for datanode_id, datanode_info in datanodes_info.items():
            last_heartbeat_time = datanode_info['last_heartbeat']
            print('cualquier: ',current_time - last_heartbeat_time)
            if current_time - last_heartbeat_time > max_inactive_time:
                datanodes_info[datanode_id]['status'] = 'inactive'
        time.sleep(10)

if __name__ == '__main__':
    check_status_thread = threading.Thread(target=check_datanode_status)
    check_status_thread.start()
    app.run(debug=True)
