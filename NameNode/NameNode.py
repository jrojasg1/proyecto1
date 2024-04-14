import time
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


datanodes_info = {}
chunk_paths = {}

@app.route('/datanodes', methods=['GET'])
def get_datanode_info():
    try:
        response = requests.get('http://localhost:5000/ping')
        
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
    datanodes_info[datanode_id] = {
        'id': datanode_id,
        'address': datanode_address,
        'address_rest': datanode_address_rest,
        'capacity': datanode_capacity,
        'rack': datanode_rack
    }
    return jsonify({'message': 'DataNode registrado exitosamente'})

# Endpoint para recibir la ruta de un chunk y almacenarla en el NameNode
@app.route('/chunk', methods=['POST'])
def register_chunk_path():
    data = request.json
    
    datanode_address = data.get('datanode_address')
    chunk_path = data.get('chunk_path')
    # Almacenar la ruta del chunk en la estructura de datos asociada a la dirección del DataNode
    if datanode_address in chunk_paths:
        chunk_paths[datanode_address].append(chunk_path)
    else:
        chunk_paths[datanode_address] = [chunk_path]
    print('chunk_paths: ', chunk_paths)
    return jsonify({'message': 'Ruta del chunk almacenada exitosamente'})

# Endpoint para hacer ping al DataNode y medir el tiempo de respuesta
@app.route('/ping', methods=['GET'])
def ping_datanode():
    try:
        min_ping_time = float('inf')  # Inicializar el tiempo de ping mínimo como infinito
        fastest_datanode = None  # Inicializar el datanode más rápido como None
        
        for datanode_id, datanode_info in datanodes_info.items():
            
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


if __name__ == '__main__':
    app.run(debug=True)
