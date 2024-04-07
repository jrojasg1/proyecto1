import json
from flask import Flask, jsonify
#import namenode_pb2
#import namenode_pb2_grpc

app = Flask(__name__)

# Cargar la configuración de los DataNodes desde el archivo JSON
def load_datanodes_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    return config["datanodes"]

# Obtener información de un DataNode específico
@app.route('/datanodes', methods=['GET'])
def get_datanode_info():
    datanodes = load_datanodes_config("datanodes.json")
    if datanodes:
        # En este ejemplo, simplemente se devuelve el primer DataNode de la lista
        return jsonify(datanodes[1])
    else:
        return jsonify({"error": "No hay DataNodes disponibles"}), 404
@app.route('/num_chunks', methods=['POST'])
def handle_num_chunks():
    data = request.json
    filename = data.get('filename')
    chunk_index = data.get('chunk_index')
    num_chunks = data.get('num_chunks')

    #DataNode guardar el chunk
    
    datanode_id = 1

    return jsonify({'datanode_id': datanode_id})

if __name__ == '__main__':
    app.run(debug=True)
