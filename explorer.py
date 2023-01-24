from flask import Flask, render_template, request
from miner import Miner, Wallet
import uuid

app = Flask(__name__)

wallet = Wallet()
miner = Miner(uuid.UUID(int=uuid.getnode()))

@app.route('/')
def index():
    return render_template('index.html', blockchain=miner.blockchain.blockchain)

@app.route('/transaction', methods=['POST'])
def transaction():
    recipient = request.form['recipient']
    amount = request.form['amount']
    
    transaction = wallet.create_transaction(recipient, amount)
    wallet.send_transaction(transaction, miner)
    return 'Transaction posted'

@app.route('/is_valid', methods=['GET'])
def is_valid():
    if miner.blockchain.is_valid():
        return "Blockchain is valid"
    else:
        return "Blockchain is not valid"

if __name__ == '__main__':
    app.run(debug=True)