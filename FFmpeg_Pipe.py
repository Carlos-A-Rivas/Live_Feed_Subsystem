import subprocess
from flask import Flask, Response, render_template

app = Flask(__name__)
stream_path = 'prototypeStream'
RTSP_URL = f"rtsp://172.20.10.10:8554/{stream_path}"

def gen_mjpeg():
    # force TCP transport, scale to 640×360, 10 FPS, quality=5
    cmd = [
        "ffmpeg",
        "-rtsp_transport", "tcp",
        "-i", RTSP_URL,
        "-vf", "scale=640:360",
        "-r", "10",
        "-q:v", "5",
        #"-c", "copy",
        "-f", "mjpeg",
        "pipe:1"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return proc.stdout

@app.route("/video_feed")
def video_feed():
    return Response(
        gen_mjpeg(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # host=0.0.0.0 makes it visible to a LAN
    app.run(host="0.0.0.0", port=5000)
