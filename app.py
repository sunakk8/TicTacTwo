from flask import Flask, request
from flask_socketio import SocketIO, emit

#Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Flask SocketIO server is running"

@socketio.on("connect")
def handle_connect():
    socket_id = request.sid
    print(f"A user connected with socket ID: {socket_id}")
    
    # Send the socket ID back to the client
    emit('socket_id', {'socket_id': socket_id})

@socketio.on("disconnect")
def handle_disconnect():
    print("A user disconnected")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)