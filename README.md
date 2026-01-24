Markdown

# 🛡️ Smart Shop Security System

A comprehensive, computer-vision-based security solution designed for after-hours shop protection. This system detects intruders using Artificial Intelligence (YOLOv3) and instantly notifies business owners via **SMS** and **Email** with photographic evidence.

![Project Status](https://img.shields.io/badge/Status-Prototype-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![OpenCV](https://img.shields.io/badge/CV-OpenCV-red)

## 📖 Overview

Traditional security cameras are passive,they record crimes but don't stop them. This project builds a **Proactive Security System** that acts as a virtual guard.

When the system is **ARMED** (e.g., when the shop is closed), it monitors the video feed for human presence. If an intruder is detected, the system locks the evidence and triggers a dual-alert mechanism to ensure the owner is notified immediately, regardless of where they are.

## ✨ Key Features

*   **🕵️ Real-Time Human Detection:** Uses the YOLOv3 (You Only Look Once) AI model to detect humans while ignoring false positives like pets or moving shadows.
*   **📱 Instant SMS Alerts:** Integrated with **Twilio** to send immediate text notifications to the owner's mobile.
*   **📧 Email Evidence:** Automatically captures a high-quality snapshot of the intruder and sends it as an email attachment.
*   **💻 Web Control Panel:** A responsive Dashboard (Flask) to view the live feed and system status.
*   **🛡️ Secure Logic:**
    *   **Arm/Disarm System:** The owner activates the AI only when the shop is closed.
    *   **User Authentication:** Secure Login/Signup system to prevent unauthorized access.
    *   **Database:** SQLite database to manage users and potential logs.

## 🛠️ Tech Stack

*   **Backend:** Python (Flask Framework)
*   **Computer Vision:** OpenCV, YOLOv3 (Deep Neural Network)
*   **Database:** SQLite (via SQLAlchemy)
*   **Notifications:** Twilio API (SMS), Python `smtplib` (Email)
*   **Frontend:** HTML5, CSS3, JavaScript (jQuery)

## ⚙️ Installation & Setup
```bash

 1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/Smart-Shop-Security-System.git
cd Smart-Shop-Security-System
2. Install Dependencies
Bash

pip install -r requirements.txt
⚠️ 3. Download YOLO Weights (Important)
Due to GitHub file size limits, the AI model weights are not included in this repo.

Download the file (237 MB) from here: https://pjreddie.com/media/files/yolov3.weights
Place the file inside the root folder of this project.
Ensure your folder contains: yolov3.weights, yolov3.cfg, and coco.names.

4. Configure Environment Variables
Create a file named .env in the root directory (do not upload this file). Add your credentials:

ini

# Email Settings (Gmail App Password)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

# Twilio SMS Settings
TWILIO_SID=ACxxxxxxxxxxxxxxxx
TWILIO_TOKEN=your_auth_token
TWILIO_FROM=+8000000000
TWILIO_TO=+80000000000

# Flask Security
SECRET_KEY=supersecretkey123
5. Run the Application
Bash

python app.py
Access the dashboard at: http://127.0.0.1:5000

📸 Usage Workflow
Login to the system using secure credentials.
View the Live Feed to ensure the shop is empty.
Click "ARM SYSTEM" before leaving the shop.
If anyone enters, you receive an SMS and an Email with their photo immediately.
Login remotely to view the incident history or Disarm.
🚀 Future Roadmap
This project is currently in the Demo/Prototype phase. Future improvements planned before final release:

 Integration with Raspberry Pi 5 for a standalone device.
 Cloud Storage (AWS S3/Firebase) for incident history.
 Face Recognition to automatically whitelist employees.
 Telegram Bot integration for remote control.
🤝 Contributing
This is an academic project. Feedback and suggestions are welcome!

📄 License
Distributed under the MIT License.
