import subprocess

def start_stream(pre_recorded_video_path="/home/cariv/Downloads/Test_Vid_15FPS.mp4", stream_path="/prototypeStream"):
    """
    This function starts streaming a pre-recorded video over RTSP.
    
    Parameters:
      pre_recorded_video_path: Path to your video file.
      stream_path: The endpoint path on the RTSP server.
      
    Returns:
      A subprocess.Popen object representing the FFmpeg process.
    """
    # Construct the RTSP URL. Replace 'localhost' with your Pi’s IP if needed.
    rtsp_url = f"rtsp://172.20.10.10:8554{stream_path}"
    # IP: 10.200.97.153
    
    # FFmpeg command breakdown:
    # -re                : Read input at native frame rate (simulate live streaming).
    # -i <file>          : Input file (your pre-recorded video).
    # -c copy            : Copy the input video/audio streams without re-encoding.
    # -f rtsp            : Set the output format to RTSP.
    command = [
        "ffmpeg",
        "-stream_loop", "-1",  # This flag makes FFmpeg loop the input endlessly.
        "-re",
        "-i", pre_recorded_video_path,
        "-c", "copy",
        "-f", "rtsp",
        #"-rtsp_flags", "listen+prefer_tcp",
        "-rtsp_transport", "tcp",
        rtsp_url
    ]
    
    print(f"Starting stream: {rtsp_url}")
    # Launch the FFmpeg process.
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

if __name__ == "__main__":
    # Start streaming the pre-recorded video.
    stream_process = start_stream()
    
    try:
        stream_process.wait()
    except KeyboardInterrupt:
        print("Stream stopped by user.")
        stream_process.terminate()
