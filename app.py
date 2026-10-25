import cv2
import numpy as np
import serial
import time
import os
import requests

# --- TELEGRAM CONFIGURATION ---
TELEGRAM_TOKEN = "8463398369:AAE3fOr1nDywfA8DLBJW4ODkI3sEa8hTQAw"      # Paste your BotFather token here
TELEGRAM_CHAT_ID = "1924296372"    # Paste your UserInfoBot ID here
last_notification_time = 0
from flask import Flask, render_template_string, Response, jsonify

app = Flask(__name__)

ARDUINO_PORT = 'COM7' 
BAUD_RATE = 9600

try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Arduino connected successfully.")
except Exception as e:
    print(f"Warning: Could not connect to Arduino: {e}")
    arduino = None

# Ensure static folder exists and create a default placeholder image safely
if not os.path.exists('static'):
    os.makedirs('static')

default_img_path = os.path.join('static', 'default.jpg')
if not os.path.exists(default_img_path):
    blank_img = np.zeros((300, 400, 3), dtype=np.uint8)
    cv2.putText(blank_img, "Waiting For Fire Event...", (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (148, 163, 184), 2)
    cv2.imwrite(default_img_path, blank_img)

alert_status = "System Normal - Monitoring..."
latest_fire_image = default_img_path
last_alert_time = 0

def detect_fire_in_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_fire = np.array([18, 50, 50], dtype=np.uint8)
    upper_fire = np.array([35, 255, 255], dtype=np.uint8)
    
    mask = cv2.inRange(hsv, lower_fire, upper_fire)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    fire_detected = False
    for c in contours:
        if cv2.contourArea(c) > 1000:
            fire_detected = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "FIRE DETECTED!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            
    return frame, fire_detected
def send_telegram_alert(image_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    try:
        with open(image_path, 'rb') as photo:
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': '🚨 EMERGENCY: Fire Detected by AI System!'
            }
            files = {'photo': photo}
            requests.post(url, data=payload, files=files, timeout=5)
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")

def generate_frames():
    global alert_status, latest_fire_image, last_alert_time

def generate_frames():
    global alert_status, latest_fire_image, last_alert_time
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        processed_frame, fire_detected = detect_fire_in_frame(frame)
        current_time = time.time()
        
        if fire_detected:
            alert_status = "⚠️ ALERT: Fire Detected!"
            last_alert_time = current_time
            
            filename = os.path.join('static', f"fire_alert_{int(current_time)}.jpg")
            cv2.imwrite(filename, processed_frame)
            latest_fire_image = filename
            
            global last_notification_time
            if current_time - last_notification_time > 30:
                send_telegram_alert(filename)
                last_notification_time = current_time
            
            if arduino:
                arduino.write(b'H')
        else:
            if current_time - last_alert_time > 2:
                alert_status = "System Normal - Monitoring..."
                if arduino:
                    arduino.write(b'L')

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Fire Command & Defense System</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #07090e;
            --bg-card: #111827;
            --border-color: #1f293d;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-glow: rgba(239, 68, 68, 0.25);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            margin: 0;
            padding: 30px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
        }

        h1 {
            margin: 0;
            font-size: 2.4rem;
            font-weight: 700;
            letter-spacing: 2px;
            background: linear-gradient(135deg, #f59e0b, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }

        p.subtitle {
            color: var(--text-muted);
            margin-top: 8px;
            font-size: 0.95rem;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.5px;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 25px;
            width: 100%;
            max-width: 1300px;
        }

        @media(max-width: 900px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background-color: var(--bg-card);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
            border: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
        }

        .card-header h3 {
            margin: 0;
            color: var(--text-muted);
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .live-dot {
            width: 10px;
            height: 10px;
            background-color: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-green);
            animation: pulse-dot 2s infinite;
        }

        @keyframes pulse-dot {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        .feed-container {
            width: 100%;
            border-radius: 10px;
            overflow: hidden;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 1px solid var(--border-color);
        }

        img {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 8px;
        }

        .status-badge {
            padding: 16px;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: 1px;
            margin-bottom: 20px;
            font-family: 'JetBrains Mono', monospace;
            transition: all 0.3s ease;
        }

        .status-normal {
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--accent-green);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .status-alert {
            background-color: rgba(239, 68, 68, 0.15);
            color: var(--accent-red);
            border: 1px solid var(--accent-red);
            box-shadow: 0 0 25px var(--accent-glow);
            animation: pulse-glow 1s infinite alternate;
        }

        @keyframes pulse-glow {
            0% { box-shadow: 0 0 10px rgba(239, 68, 68, 0.3); }
            100% { box-shadow: 0 0 25px rgba(239, 68, 68, 0.8); }
        }

        .specs-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 20px;
        }

        .spec-box {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            padding: 14px;
            border-radius: 10px;
            text-align: center;
        }

        .spec-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }

        .spec-value {
            font-size: 0.95rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
            color: #fff;
        }

        .evidence-card {
            background: rgba(239, 68, 68, 0.04);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 12px;
            padding: 16px;
            margin-top: auto;
            display: none;
            animation: fadeIn 0.4s ease-in-out;
        }

        .evidence-card.visible {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .evidence-title {
            color: var(--accent-red);
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
    </style>
</head>
<body>

    <header>
        <h1>AI Fire Command System</h1>
        <p class="subtitle">Autonomous Computer Vision // Hardware Actuation // Telemetry</p>
    </header>

    <div class="dashboard-grid">
        <div class="card">
            <div class="card-header">
                <h3>Live Optical Feed</h3>
                <div class="live-dot"></div>
            </div>
            <div class="feed-container">
                <img src="/video_feed" alt="Live Surveillance Feed">
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h3>System Telemetry</h3>
                <span style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: var(--accent-green);">ONLINE</span>
            </div>

            <div id="status" class="status-badge status-normal">
                {{ status }}
            </div>

            <div class="specs-grid">
                <div class="spec-box">
                    <div class="spec-label">Hardware Link</div>
                    <div class="spec-value" style="color: var(--accent-green);">CONNECTED (COM7)</div>
                </div>
                <div class="spec-box">
                    <div class="spec-label">Mobile Protocol</div>
                    <div class="spec-value" style="color: #38bdf8;">TELEGRAM ACTIVE</div>
                </div>
                <div class="spec-box">
                    <div class="spec-label">Algorithm</div>
                    <div class="spec-value">HSV Color Matrix</div>
                </div>
                <div class="spec-box">
                    <div class="spec-label">Response Time</div>
                    <div class="spec-value">&lt; 50ms</div>
                </div>
            </div>

            <div id="evidence-panel" class="evidence-card">
                <div class="evidence-title">
                    <span>🔴</span> Critical Incident Snapshot Captured
                </div>
                <div class="feed-container">
                    <img id="snapshot-img" src="/snapshot" alt="Fire Incident Evidence">
                </div>
            </div>
        </div>
    </div>

    <script>
        setInterval(() => {
            fetch('/status')
                .then(res => res.json())
                .then(data => {
                    const statusDiv = document.getElementById('status');
                    const evidencePanel = document.getElementById('evidence-panel');
                    const snapshotImg = document.getElementById('snapshot-img');
                    
                    if (data.status !== statusDiv.innerText) {
                        statusDiv.innerText = data.status;
                        if (data.status.includes('ALERT')) {
                            statusDiv.className = 'status-badge status-alert';
                            evidencePanel.classList.add('visible');
                        } else {
                            statusDiv.className = 'status-badge status-normal';
                        }
                    }
                    
                    if (data.has_alert) {
                        evidencePanel.classList.add('visible');
                        const targetSrc = '/snapshot?' + data.latest_image;
                        if (snapshotImg.getAttribute('src').split('?')[1] !== data.latest_image) {
                            snapshotImg.src = targetSrc;
                        }
                    }
                });
        }, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE, status=alert_status)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/snapshot')
def snapshot():
    from flask import send_file
    if os.path.exists(latest_fire_image):
        return send_file(latest_fire_image, mimetype='image/jpeg')
    return send_file(default_img_path, mimetype='image/jpeg')

@app.route('/status')
def status():
    return jsonify({"status": alert_status, "latest_image": latest_fire_image})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=True)