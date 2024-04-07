import json
from flask import Flask, jsonify
#import namenode_pb2
#import namenode_pb2_grpc

app = Flask(__name__)

def load_datanodes_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    return config["datanodes"]

@app.route('/datanodes', methods=['GET'])
def get_datanode_info():
    datanodes = load_datanodes_config("datanodes.json")
    if datanodes:
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
