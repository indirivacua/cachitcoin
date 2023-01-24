import ecdsa
from blockchain import Blockchain

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.generate_keys()

    def generate_keys(self):
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()
        self.private_key = private_key
        self.public_key = public_key

    def create_transaction(self, recipient, amount):
        transaction = {
            'sender': self.public_key.to_string().hex(),
            'recipient': recipient,
            'amount': amount
        }
        # sign the transaction
        signature = self.private_key.sign(str(transaction).encode())
        transaction['signature'] = signature.hex()
        return transaction
    
    def send_transaction(self,transaction,miner):
        miner.add_transaction(transaction)

class Miner:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = []
        self.blockchain = Blockchain()

    def add_coins(self, amount):
        self.balance += amount

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        if len(self.transactions) >= 1024:
            self.blockchain.add_block("", self, self.transactions)
            self.transactions = []

if __name__ == "__main__":
  w1 = Wallet()
  w2 = Wallet()
  m = Miner("cacho")

  for i in range(1024):
    t1 = w1.create_transaction(w2.public_key, 1/(i+1))
    w1.send_transaction(t1, m)
  
  for block in m.blockchain.blockchain:
    print("timestamp: {0}\ndata: {1}\nnonce: {2}\nminer: {3}\ntransactions: {4}\nnumber of transactions: {5}\nhash: {6}\n"
    .format(block.timestamp, 
            block.data, 
            block.nonce, 
            block.miner.name if block.miner else "None", 
            "",#block.transactions, 
            block.number_of_transactions, 
            block.hash)
    )

  print(m.blockchain.is_valid())
  print(m.blockchain.block_count, m.balance)
  