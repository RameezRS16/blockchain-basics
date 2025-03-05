from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)

# Blockchain ka instance create karna
my_blockchain = Blockchain()

# API Endpoints

@app.route('/blocks', methods=['GET'])
def get_blocks():
    chain_data = []
    for block in my_blockchain.chain:
        chain_data.append({
            "index": block.index,
            "previous_hash": block.previous_hash,
            "data": block.data,
            "timestamp": block.timestamp,
            "hash": block.hash
        })
    return jsonify({"length": len(chain_data), "chain": chain_data})

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json.get("data", "")
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    my_blockchain.add_block(data)
    return jsonify({"message": "Block added successfully", "new_block": my_blockchain.chain[-1].__dict__})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
