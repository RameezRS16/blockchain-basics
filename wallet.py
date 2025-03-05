from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class Wallet:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def get_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    def sign_transaction(self, transaction_data):
        signature = self.private_key.sign(
            transaction_data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, public_key_pem, transaction_data, signature):
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        try:
            public_key.verify(
                signature,
                transaction_data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False

# Testing Wallet System
if __name__ == "__main__":
    wallet = Wallet()
    public_key = wallet.get_public_key()

    transaction_data = "Alice sends 10 coins to Bob"
    signature = wallet.sign_transaction(transaction_data)

    # Verify Transaction
    is_valid = wallet.verify_signature(public_key, transaction_data, signature)
    print(f"Transaction Valid: {is_valid}")
