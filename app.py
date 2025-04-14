from flask import Flask, render_template, Response, request, send_file
from finger_canvas import FingerCanvas
import time
import io

app = Flask(__name__)
canvas = FingerCanvas()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        frame, _ = canvas.process_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.05)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/clear', methods=['POST'])
def clear_canvas():
    canvas.clear_canvas()
    return '', 204

@app.route('/save_image')
def save_image():
    _, canvas_img = canvas.process_frame()
    return send_file(
        io.BytesIO(canvas_img),
        mimetype='image/png',
        as_attachment=True,
        download_name='drawing.png'
    )

@app.route('/change_color', methods=['POST'])
def change_color():
    color = request.form.get('color')
    canvas.change_color(color)
    return '', 204

@app.route('/change_brush', methods=['POST'])
def change_brush():
    size = int(request.form.get('size'))
    canvas.change_brush_size(size)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)