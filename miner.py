class Miner:
    def __init__(self, name):
        self.name = name
        self.balance = 0

    def add_coins(self, amount):
        self.balance += amount