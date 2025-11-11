# 🧍‍♂️ Fall Detection System using YOLOv8 Pose  
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)  
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)  
![Ultralytics YOLOv8](https://img.shields.io/badge/YOLOv8-Pose-orange)  
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🧠 Overview  
This project implements a **real-time fall detection system** using the **YOLOv8 Pose Estimation model**.  
It detects human postures from a video feed, analyzes pose keypoints, and sends **instant alerts** through the **Pushover** notification API when a fall is detected.

---

## 🎯 Features  
✅ Real-time human pose tracking using YOLOv8  
✅ Calculates **torso angle** and **aspect ratio** to detect falls  
✅ Sends **instant alerts** via **Pushover**  
✅ Works with any camera or pre-recorded video  
✅ Lightweight and easy to deploy on edge devices  

---

## 🧩 Installation

### 
1️⃣ Clone this repository
```bash
git clone https://github.com/<your-username>/fall-detection.git
cd fall-detection

2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Download the YOLOv8 Pose model
bash
Copy code
yolo download model=yolov8n-pose.pt
Or download it manually from Ultralytics Models.

⚙️ Configuration
In the script, you can modify parameters:

python
Copy code
VIDEO_PATH = '/home/aiml/fall/two.mp4'
FALL_ANGLE_THRESHOLD = 75.0
FALL_RATIO_THRESHOLD = 0.9
CONFIDENCE_FLOOR = 0.65
These thresholds control sensitivity and accuracy.

▶️ Running the System
bash
Copy code
python fall_detection.py
Press q to quit the video window.

📲 Pushover Alert Setup
Create a free account at https://pushover.net

Obtain your User Key and API Token

Replace them in the code:

python
Copy code
USER_KEY = 'your_user_key_here'
API_TOKEN = 'your_api_token_here'
You’ll receive instant mobile/desktop alerts on fall detection.

📈 Detection Accuracy
On the provided video (two.mp4), the system achieved ~87% confidence in detecting falls.

Accuracy depends on:

Camera angle and frame rate

Lighting and background

Occlusion or multiple people

Fine-tuning thresholds can improve precision for your setup.

🎥 Demo
A short demo video (fall_detection_demo.mp4) shows:

Detection of a person’s fall

Real-time bounding boxes and labels

Pushover alert notifications

🗂️ Project Structure
bash
Copy code
fall-detection/
│
├── fall_detection.py          # Main detection script
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
├── .gitignore                 # Ignore cache/log/demo files
├── fall_detection_demo.mp4    # (Optional) Demo video
└── outputs/
    └── alerts_log.txt         # (Optional) Alert log
🧑‍💻 Author
Ram Reddy
🎓 Graduate Research Assistant, University of South Florida
💡 Machine Learning Engineer | Computer Vision | AI Systems

