from flask import Flask, Response, render_template
import cv2
import time
import subprocess
import pandas as pd

app = Flask(__name__)

# RTSP URI from your mediamtx server
stream_path="/prototypeStream"
RTSP_URL = f"rtsp://172.20.10.10:8554{stream_path}"
start_times = []
end_times = []
round_trip = []

def gen_frames():
    cap = cv2.VideoCapture(RTSP_URL)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)
    cap.set(cv2.CAP_PROP_FPS, 10)
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
    

@app.route('/start_stream')
def boot():
    global t_start
    global t_end
    global process_1
    global process_2
    t_start = time.time_ns()
    # Starts mediamtx
    command_1 = ["./mediamtx"]
    process_1 = subprocess.Popen(command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    # Starts RTSP Stream
    command_2 = ['python3', 'PPD_Prototype.py']
    process_2 = subprocess.Popen(command_2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    # Allows user to view the stream
    t_end = time.time_ns()
    print(f"Data Collected!!!!!")
    return render_template('index.html')
    
@app.route('/stop_stream')
def stop_stream():
    start_s = [t_start * (10**-9)]
    end_s = [t_end * (10**-9)]
    trip_s = [(t_end-t_start) * (10**-9)]
    print((
    f"Beginning Time Point:  {start_s}s\n"
    f"End Time Point:        {end_s}s\n"
    f"Total Connection Time:          {trip_s}s"))
    df = pd.DataFrame({
    't_start': start_s,
    't_end': end_s,
    't_l': trip_s
    })
    df.to_csv('Latency_Data.csv', mode='a', header=False, index=False)
    print(f"Data Saved!!!!!!")
    process_1.kill()
    process_2.kill()


@app.route('/')
def index():
    return render_template('index.html')
    
if __name__ == '__main__':
    # host=0.0.0.0 makes it visible to your LAN
    app.run(host='0.0.0.0', port=5000, threaded=True)
