from flask import Flask
from flask import request
import flask.json
from board import Board
from flask import render_template

app = Flask(__name__)



@app.route("/")
def index():
    return render_template('index.html')

@app.route('/board', methods=['POST'])
def board():
    grid = flask.json.loads(request.values['board'])
    board = Board(grid)
    board.move()
    ret = { 'board': board.grid, 'status': board.get_status() }
    return flask.json.dumps(ret)

if __name__ == "__main__":
    app.run(debug=True)
