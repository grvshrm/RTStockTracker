from flask import Flask, render_template, url_for, request
import requests, json
from flask_socketio import SocketIO, emit
#from flask_cors import CORS
from threading import Lock

thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
socketio = SocketIO(app, cors_allowed_origins = "*")
#socketio.init_app(app)
# CORS(app)

def background_thread():
    print("Fetching Stock Data")
    while True:
        response = requests.get("http://localhost:4000/getdata")
        stockdata = response.json()
        socketio.emit('updateStockData', stockdata)
        socketio.sleep(1)

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@socketio.on('connect')
def connect():
    global thread
    print('Client Connected!')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    print("Client Disconnected -", request.sid)

if __name__ == "__main__":
    # app.run(debug = True)
    socketio.run(app)