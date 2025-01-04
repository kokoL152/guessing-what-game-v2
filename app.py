from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import json

app = Flask(__name__, static_url_path='/static', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")
rooms = {}

# @app.route('/')
# def home():
#     return render_template('index.html')

@socketio.on('draw')
def handle_draw(data):
    emit('draw', data, broadcast=True)

@socketio.on('clear_canvas')
def handle_clear():
    emit('clear_canvas', broadcast=True)

@app.route('/draw/<int:game_id>')
def draw(game_id):
    return render_template('index.html', game_id=game_id, role='explainer')

@app.route('/guess/<int:game_id>')
def guess(game_id):
    return render_template('guess.html', game_id=game_id, role='guesser')

@socketio.on('join')
def on_join(data):
    room = data['game_id']
    role = data['role']
    join_room(room)

    if room not in rooms:
        rooms[room] = {
            'users': 0,
            'timer': None,
            'time_left': 60,  # 60 seconds for each round
            'current_word': None,
            'game_state': 'waiting'  # Can be 'waiting', 'playing', 'finished'
        }
    rooms[room]['users'] += 1
    print("\n\n\n hi")
    print(rooms[room]["users"])
    print(role)
    
    # Notify others in the room about the new peer
    print("User joined\n")
    emit('user_joined', {
        'role': role,
        'count': rooms[room]['users'],
        'time_left': rooms[room]['time_left']
    }, room=room)

@socketio.on('timer_start')
def handle_timer_start(data):
    emit('timer_start', data, broadcast=True)

@socketio.on('submit_guess')
def handle_submit_guess(data):
    emit('submit_guess', data, broadcast=True)

@socketio.on("correct_guess")
def handle_correct_guess(data):
    emit("correct_guess", data, broadcast=True)

@socketio.on('disconnect')
def on_disconnect():
    for room in rooms:
        if request.sid in rooms[room]:
            rooms[room]['users'] -= 1
            if rooms[room]['users'] <= 0:
                # Clean up room if empty
                if rooms[room]['timer']:
                    rooms[room]['timer'].cancel()
                del rooms[room]
            break
        
if __name__ == '__main__':
    socketio.run(app, debug=True)
