import hashlib
import datetime

class Block:
    def __init__(self, timestamp, data, previous_hash, nonce=0, miner=None, transactions=None):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner = miner
        self.transactions = transactions or []
        self.number_of_transactions = len(self.transactions)
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        transactions_str = '-'.join([str(tx) for tx in self.transactions])
        hash_str = f"{self.timestamp}-{self.data}-{self.previous_hash}-{self.nonce}-{self.miner}-{transactions_str}-{self.number_of_transactions}".encode('utf-8')
        sha.update(hash_str)
        return sha.hexdigest()

class Blockchain:
    def __init__(self, difficulty=2, coin_reward=50):
        self.blockchain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.coin_reward = coin_reward
        self.halving_interval = 210000
        self.block_count = 1

    def create_genesis_block(self):
        return Block("01/01/1970", "Genesis block", "0")

    def add_block(self, data, miner, transactions):
        previous_hash = self.blockchain[-1].hash
        timestamp = datetime.datetime.now()
        nonce = 0
        # TODO check if sender have enough balance
        new_block = Block(timestamp, data, previous_hash, nonce, miner, transactions)
        new_block.hash = new_block.calc_hash()
        while not new_block.hash.startswith('0' * self.difficulty):
            nonce += 1
            new_block = Block(timestamp, data, previous_hash, nonce, miner, transactions)
            new_block.hash = new_block.calc_hash()
        self.blockchain.append(new_block)
        self.block_count += 1
        if self.block_count % self.halving_interval == 0:
            self.coin_reward = self.coin_reward / 2
        # Give the miner the coin reward
        miner.add_coins(self.coin_reward)

    def is_valid(self):
        for i in range(1, len(self.blockchain)):
            current_block = self.blockchain[i]
            previous_block = self.blockchain[i-1]
            if current_block.hash != current_block.calc_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True