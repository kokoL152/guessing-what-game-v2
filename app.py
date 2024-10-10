from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('draw')
def handle_draw(data):
    emit('draw', data, broadcast=True)

@socketio.on('clear_canvas')
def handle_clear():
    emit('clear_canvas', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
