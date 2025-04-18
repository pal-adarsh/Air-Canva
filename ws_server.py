from flask_socketio import SocketIO, emit
from flask import Flask
from finger_canvas import FingerCanvas
import cv2
import base64

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
canvas = FingerCanvas()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('clear')
def handle_clear():
    canvas.clear_canvas()

@socketio.on('change_color')
def handle_color_change(color):
    canvas.change_color(color)

@socketio.on('change_brush')
def handle_brush_change(size):
    canvas.change_brush_size(int(size))

def video_stream():
    while True:
        frame, canvas_img = canvas.process_frame()
        if frame:
            # Convert frame to base64 for WebSocket
            frame_b64 = base64.b64encode(frame).decode('utf-8')
            socketio.emit('video_frame', {'frame': frame_b64})

if __name__ == '__main__':
    socketio.start_background_task(video_stream)
    socketio.run(app, host='0.0.0.0', port=5000)