# 🛡️ Smart Shop Security System

A comprehensive, computer-vision-based security solution designed for after-hours shop protection. This system detects intruders using Artificial Intelligence (YOLOv3) and instantly notifies business owners via **SMS** and **Email** with photographic evidence.

![Project Status](https://img.shields.io/badge/Status-Prototype-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![OpenCV](https://img.shields.io/badge/CV-OpenCV-red)

## 📖 Overview

Traditional security cameras are passive—they record crimes but don't stop them. This project builds a **Proactive Security System** that acts as a virtual guard.

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

### 1. Clone the Repository
```bash
git clone https://github.com/pervejrony27/Smart-Shop-Security-System.git
cd Smart-Shop-Security-System

Due to GitHub file size limits, the AI model weights are not included in this repo.

Download the file (237 MB) from here: https://pjreddie.com/media/files/yolov3.weights
Place the file inside the root folder of this project.
Ensure your folder contains: yolov3.weights, yolov3.cfg, and coco.names.
