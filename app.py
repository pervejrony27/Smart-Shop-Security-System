import cv2
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import numpy as np
import time
import os
import threading
from flask import Flask, render_template, request, jsonify, url_for, Response

# --- CONFIGURATION ---
CONF_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4

# Email / SMS Credentials
SENDER_EMAIL = # use your email here to send alerts
SENDER_PASSWORD =  # Make sure this is your 16-char App Password
RECIPIENT_EMAIL = #Use your email here to receive alerts

# Twilio (Optional - leave blank if not using)
TWILIO_ACCOUNT_SID = "" 
TWILIO_AUTH_TOKEN = ""           
TWILIO_PHONE_NUMBER = ""                  
RECIPIENT_PHONE_NUMBER = ""              

# YOLO Files
YOLO_CFG = 'yolov3.cfg'
YOLO_WEIGHTS = 'yolov3.weights' 
YOLO_NAMES = 'coco.names'

NOTIFICATION_COOLDOWN = 15 # Seconds

# Absolute path for images to prevent "File Not Found" errors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCIDENT_IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'images')
if not os.path.exists(INCIDENT_IMAGES_DIR):
    os.makedirs(INCIDENT_IMAGES_DIR)

# --- GLOBALS ---
is_armed = False
last_notification_time = 0
output_frame = None
lock = threading.Lock()

# --- EMAIL FUNCTION ---
def send_email_alert(recipient, subject, body, image_path):
    print(f"Attempting to send email to {recipient}...")
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach Image
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as attachment:
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(image_path)}")
                msg.attach(p)
        else:
            print(f"Error: Image file not found at {image_path}")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        server.quit()
        print("✅ Email Sent Successfully!")
    except Exception as e:
        print(f"❌ Email Failed: {e}")

# --- DETECTION THREAD ---
def detection_loop():
    global output_frame, is_armed, last_notification_time

    # 1. Load YOLO (Safe Mode)
    print("Loading YOLO models...")
    net = None
    classes = []
    output_layers = []
    try:
        net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
        with open(YOLO_NAMES, 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        try:
            output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        except:
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        print("✅ YOLO Loaded Successfully.")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Could not load YOLO. Check filenames! {e}")
        print("⚠️ Camera will run, but detection is DISABLED.")
        net = None # Disable detection

    # 2. Open Camera
    # Try index 0, then index 1 if 0 fails
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("⚠️ Camera 0 failed. Trying Camera 1...")
        camera = cv2.VideoCapture(1)
        if not camera.isOpened():
            print("❌ CRITICAL ERROR: No Camera found!")
            return

    print("✅ Camera Started. Frame processing loop begin.")

    while True:
        success, frame = camera.read()
        if not success:
            print("⚠️ Failed to read frame from camera. Retrying...")
            time.sleep(1)
            continue

        # Copy frame for processing
        display_frame = frame.copy()

        # Only run detection if ARMED and YOLO is loaded
        if is_armed and net is not None:
            height, width, _ = frame.shape
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            
            # This line does the heavy AI math
            outs = net.forward(output_layers)

            class_ids = []
            confidences = []
            boxes = []

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    # Check if it is a 'person' (index 0 in COCO)
                    if confidence > CONF_THRESHOLD and classes[class_id] == 'person':
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)

            if len(indexes) > 0:
                # PERSON DETECTED
                current_time = time.time()
                
                # Draw Box
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(display_frame, "INTRUDER", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

                # Check Cooldown before emailing
                if current_time - last_notification_time > NOTIFICATION_COOLDOWN:
                    last_notification_time = current_time
                    
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"incident_{timestamp}.jpg"
                    filepath = os.path.join(INCIDENT_IMAGES_DIR, filename)
                    
                    # Save Image
                    cv2.imwrite(filepath, display_frame)
                    print(f"📸 Intruder detected! Saved: {filepath}")
                    
                    # Send Email in a separate short-lived thread to not block video
                    email_t = threading.Thread(target=send_email_alert, args=(
                        RECIPIENT_EMAIL, 
                        f"SECURITY ALERT {timestamp}", 
                        "A human presence has been detected by your shop during off hours.Take action immediately!.see attached image for evidence.", 
                        filepath
                    ))
                    email_t.start()
        
        elif is_armed and net is None:
            # Armed but YOLO broken
            cv2.putText(display_frame, "ERROR: YOLO NOT LOADED", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        # Update the global frame for the web browser
        with lock:
            output_frame = display_frame.copy()
        
        time.sleep(0.01) # Small sleep to save CPU

# --- FLASK APP ---
app = Flask(__name__)

def generate_frames():
    global output_frame
    while True:
        with lock:
            if output_frame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    # Return list of images
    images = []
    try:
        files = sorted(os.listdir(INCIDENT_IMAGES_DIR), reverse=True)
        for f in files:
            if f.endswith('.jpg'):
                images.append({
                    "url": url_for('static', filename=f'images/{f}'),
                    "timestamp": f
                })
    except:
        pass
    return jsonify({"is_armed": is_armed, "all_incidents": images})

@app.route('/arm', methods=['POST'])
def arm():
    global is_armed
    is_armed = True
    print("🛡️ System ARMED")
    return jsonify({"message": "System Armed"})

@app.route('/disarm', methods=['POST'])
def disarm():
    global is_armed
    is_armed = False
    print("🏳️ System DISARMED")
    return jsonify({"message": "System Disarmed"})

if __name__ == '__main__':
    t = threading.Thread(target=detection_loop, daemon=True)
    t.start()
    
    print(f"Server starting at http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)