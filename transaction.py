import hashlib
import json
import time

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
        self.transaction_id = self.calculate_transaction_id()

    def calculate_transaction_id(self):
        transaction_data = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return hashlib.sha256(transaction_data.encode()).hexdigest()

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "transaction_id": self.transaction_id
        }

# Testing Transaction Class
if __name__ == "__main__":
    txn1 = Transaction("Alice", "Bob", 50)
    print(json.dumps(txn1.to_dict(), indent=4))
