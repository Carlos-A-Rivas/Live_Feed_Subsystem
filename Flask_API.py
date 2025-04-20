from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

# RTSP URI from your mediamtx server
RTSP_URL = "rtsp://localhost:8554/mystream"

def gen_frames():
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open RTSP stream: {RTSP_URL}")

    while True:
        success, frame = cap.read()
        if not success:
            break

        # encode as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # yield multipart
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
        )

@app.route('/video_feed')
def video_feed():
    return Response(
        gen_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/')
def index():
    return render_template('/templates/index.html')
    
if __name__ == '__main__':
    # host=0.0.0.0 makes it visible to your LAN
    app.run(host='0.0.0.0', port=5000, threaded=True)
