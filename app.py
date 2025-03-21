from flask import Flask, render_template
from flask_socketio import SocketIO
from pynput import mouse
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Global variable to store mouse position
mouse_position = {"x": 0, "y": 0}

# Mouse movement listener
def on_move(x, y):
    global mouse_position
    mouse_position = {"x": x, "y": y}

listener = mouse.Listener(on_move=on_move)
listener.start()

@app.route("/")
def index():
    return render_template("index.html")

# Function to emit mouse position updates
def emit_mouse_position():
    while True:
        socketio.emit("mouse_position", mouse_position)
        socketio.sleep(0.1)  # Emit updates every 100ms

if __name__ == "__main__":
    # Start the mouse position emitter in a separate thread
    threading.Thread(target=emit_mouse_position, daemon=True).start()
    socketio.run(app, debug=True)