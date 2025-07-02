from flask import Flask, render_template, Response, request
from picamera2 import Picamera2
import cv2
import threading
from motor_control import move, stop
import socket
import json
import sys

app = Flask(__name__)

# === Transmisión de cámaras ===
def generate_frames(camera_id=0):
    try:
        picam2 = Picamera2(camera_num=camera_id)
        config = picam2.create_preview_configuration(main={"size": (640, 480)})
        picam2.configure(config)
        picam2.start()
        while True:
            frame = picam2.capture_array()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(f"[Error] Cámara {camera_id}: {e}")
        sys.exit(1)

@app.route('/video_feed/<int:cam>')
def video_feed(cam):
    return Response(generate_frames(camera_id=cam), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control/<command>')
def control(command):
    speeds = {
        'forward': (100, 100),
        'backward': (-100, -100),
        'left': (-50, 50),
        'right': (50, -50),
        'stop': (0, 0)
    }
    if command in speeds:
        l, r = speeds[command]
        move(l, r)
    return "OK"

@app.route('/control/mix')
def control_mix():
    left = int(request.args.get('left', 0))
    right = int(request.args.get('right', 0))
    move(left, right)
    return "OK"

# === Recepción de joystick por UDP ===
def udp_receiver():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print("📡 Esperando comandos UDP...")

    while True:
        data, _ = sock.recvfrom(1024)
        try:
            cmd = json.loads(data.decode())
            x = float(cmd["x"])
            y = float(cmd["y"])

            left = y + x
            right = y - x

            left = max(-100, min(100, left * 100))
            right = max(-100, min(100, right * 100))

            move(left, right)
        except Exception as e:
            print(f"⚠ Error recibiendo comando: {e}")
            stop()

if __name__ == '__main__':
    # Iniciar servidor web en hilo separado
    web_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    web_thread.daemon = True
    web_thread.start()

    # Iniciar recepción de joystick
    udp_receiver()
