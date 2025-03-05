import hashlib
import time
from blockchain import Block, Blockchain

class Miner:
    def __init__(self, blockchain, difficulty=2):
        self.blockchain = blockchain
        self.difficulty = difficulty  # Number of leading zeros required in hash

    def proof_of_work(self, block):
        block_nonce = 0
        while True:
            block_content = f"{block.index}{block.previous_hash}{block.data}{block.timestamp}{block_nonce}"
            block_hash = hashlib.sha256(block_content.encode()).hexdigest()
            
            if block_hash[:self.difficulty] == "0" * self.difficulty:  # Valid hash condition
                block.hash = block_hash
                block.nonce = block_nonce
                return block

            block_nonce += 1  # Increment nonce to find valid hash

    def mine_block(self, data):
        previous_block = self.blockchain.chain[-1]
        new_block = Block(len(self.blockchain.chain), previous_block.hash, data, time.time())
        mined_block = self.proof_of_work(new_block)
        self.blockchain.chain.append(mined_block)
        return mined_block

# Testing the mining process
if __name__ == "__main__":
    my_blockchain = Blockchain()
    miner = Miner(my_blockchain, difficulty=3)  # Adjust difficulty as needed

    print("Mining new block...")
    new_block = miner.mine_block("Transaction Data")
    print(f"Block Mined: {new_block.hash}")
    print(f"Nonce: {new_block.nonce}")
