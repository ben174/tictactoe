import json

from flask import Flask
from flask import request
from flask import render_template

from board import Board

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/board', methods=['POST'])
def board():
    grid = json.loads(request.values['board'])
    board = Board(grid)
    board.move()
    ret = {'board': board.grid, 'status': board.get_status()}
    return json.dumps(ret)


if __name__ == "__main__":
    app.run(debug=True)
