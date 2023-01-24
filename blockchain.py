import hashlib
import datetime

class Block:
    def __init__(self, timestamp, data, previous_hash, nonce=0):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        hash_str = f"{self.timestamp}-{self.data}-{self.previous_hash}-{self.nonce}".encode('utf-8')
        sha.update(hash_str)
        return sha.hexdigest()

class Blockchain:
    def __init__(self, difficulty=2):
        self.blockchain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block("01/01/1970", "Genesis block", "0")

    def add_block(self, data):
        previous_hash = self.blockchain[-1].hash
        timestamp = datetime.datetime.now()
        nonce = 0
        new_block = Block(timestamp, data, previous_hash, nonce)
        new_block.hash = new_block.calc_hash()
        while not new_block.hash.startswith('0' * self.difficulty):
            nonce += 1
            new_block = Block(timestamp, data, previous_hash, nonce)
            new_block.hash = new_block.calc_hash()
        self.blockchain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.blockchain)):
            current_block = self.blockchain[i]
            previous_block = self.blockchain[i-1]
            if current_block.hash != current_block.calc_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

if __name__ == "__main__":
  b = Blockchain(difficulty=5)

  b.add_block("second block")
  b.add_block("third block")

  print(b.is_valid())