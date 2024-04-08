import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Estructura de datos para almacenar la información de los DataNodes y rutas de los chunks
datanodes_info = {}
chunk_paths = {}

# Obtener información de un DataNode específico
@app.route('/datanodes', methods=['GET'])
def get_datanode_info():
    if datanodes_info:
        # Encontrar el DataNode con la capacidad máxima
        max_capacity_datanode = max(datanodes_info.values(), key=lambda x: x['capacity'])
        return jsonify(max_capacity_datanode)
    else:
        return jsonify({"error": "No hay DataNodes disponibles"}), 404

# Endpoint para recibir la información de un DataNode y almacenarla en el NameNode
@app.route('/heartbeat', methods=['POST'])
def register_datanode():
    data = request.json
    
    datanode_id = data.get('id')
    datanode_address = data.get('address')
    datanode_capacity = data.get('capacity')
    datanode_rack = data.get('rack')
    # Almacenar la información del DataNode en la estructura de datos
    datanodes_info[datanode_id] = {
        'id':datanode_id,
        'address': datanode_address,
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

# Endpoint para obtener las rutas de los chunks de un archivo en un DataNode específico
@app.route('/chunk', methods=['GET'])
def get_chunk_paths():
    datanode_address = request.args.get('datanode_address')
    file_id = request.args.get('file_id')

    if datanode_address in chunk_paths:
        # Obtener todas las rutas de los chunks asociadas al DataNode
        all_chunk_paths = chunk_paths[datanode_address]
        if file_id in all_chunk_paths:
            # Retornar las rutas de los chunks para el archivo especificado
            return jsonify({"chunk_paths": all_chunk_paths[file_id]})
    
    return jsonify({"error": "No se encontraron rutas de chunks para el DataNode y el archivo especificados"}), 404

if __name__ == '__main__':
    app.run(debug=True)
