from flask import Flask, jsonify, request
import requests
from blockchain import Blockchain

app = Flask(__name__)

# Blockchain ka instance create karna
my_blockchain = Blockchain()
nodes = set()  # Connected nodes ki list

@app.route('/register_node', methods=['POST'])
def register_node():
    """Dusre nodes ko register karne ke liye API"""
    node_url = request.json.get("node_url")
    if not node_url:
        return jsonify({"error": "Invalid node URL"}), 400
    
    nodes.add(node_url)
    return jsonify({"message": "Node registered successfully", "nodes": list(nodes)})

@app.route('/sync_chain', methods=['GET'])
def sync_chain():
    """Network me sabse lambi blockchain fetch karna"""
    global my_blockchain
    longest_chain = None
    max_length = len(my_blockchain.chain)

    for node in nodes:
        try:
            response = requests.get(f"{node}/blocks")
            if response.status_code == 200:
                node_chain = response.json()["chain"]
                if len(node_chain) > max_length:
                    max_length = len(node_chain)
                    longest_chain = node_chain
        except requests.exceptions.RequestException:
            continue

    if longest_chain:
        my_blockchain.chain = longest_chain
        return jsonify({"message": "Blockchain updated to the longest chain"}), 200
    else:
        return jsonify({"message": "Blockchain is already the longest"}), 200

@app.route('/nodes', methods=['GET'])
def get_nodes():
    """Network ke sabhi connected nodes dikhane ke liye"""
    return jsonify({"nodes": list(nodes)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
