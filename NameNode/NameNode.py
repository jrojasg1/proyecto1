import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Estructura de datos para almacenar la información de los DataNodes
datanodes_info = {}

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

if __name__ == '__main__':
    app.run(debug=True)
