from flask import Flask, render_template
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain.blockchain)

if __name__ == '__main__':
    app.run(debug=True)