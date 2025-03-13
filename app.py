from flask import Flask, request
from flask_socketio import SocketIO, emit

#Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

players = [None, None]
player_count = 0

@app.route('/')
def index():
    return "Flask SocketIO server is running"

@socketio.on("connect")
def handle_connect():
    global player_count

    if player_count < 2:
        user = 0
        if (players[0] == None):
            players[0] = request.sid 
            user = 1
            print("Player 1 Connected")

        elif (players[1] == None):
            players[1] = request.sid
            print("Player 2 Connected")
            user = 2

        player_count += 1
        print(players)
        emit("player_connected", {"players": players, "user": user}, broadcast=True)

    else:
        emit("room_full", {"message": "Game is full. Try again later."})
        print("A user tried to connect, but the game is full.")

@socketio.on("disconnect")
def handle_disconnect():
    global player_count
    player_count -= 1
    if request.sid == players[0]:
        players[0] = None

    elif request.sid == players[1]:
        players[1] = None

    emit("player_disconnected", {"players": players}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)