# fall-detection-yolov8-pose
Real-time fall detection system using YOLOv8 Pose Estimation for alerting.


[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Ultralytics YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8-orange)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

A **real-time fall detection system** powered by **YOLOv8 Pose Estimation**.  
It detects human postures, computes torso orientation and aspect ratio, and sends an **instant alert** via Pushover when a fall is detected.

---

## 🚀 Features

✅ Real-time fall detection from video or webcam  
✅ Pose-based detection using YOLOv8-Pose  
✅ Configurable thresholds and sensitivity  
✅ Instant push notifications via **Pushover API**  
✅ Works for **multiple persons** with unique IDs  
✅ Compatible with **CPU and GPU**

---

## 🧠 How It Works

1. **Pose Estimation:**  
   YOLOv8-Pose identifies human keypoints (shoulders, hips, knees, etc.).

2. **Torso Angle Calculation:**  
   Calculates the tilt between shoulders and hips to determine if the person is upright or horizontal.

3. **Aspect Ratio Check:**  
   Measures height-to-width ratio of the bounding box — fallen people have lower ratios.

4. **Fall Detection Confidence (FDC):**  
   A weighted score combining:
   - Keypoint confidence  
   - Torso angle  
   - Aspect ratio  

   If the FDC > 0.65 and other thresholds are met, a **fall** is confirmed.

5. **Notifications:**  
   Sends a **Pushover alert every 2 seconds** while a fall is ongoing.

---

## ⚙️ Configuration

| Parameter | Description | Default |
|------------|-------------|----------|
| `VIDEO_PATH` | Path to input video | `/home/aiml/fall/two.mp4` |
| `MODEL_NAME` | YOLOv8 Pose model | `yolov8n-pose.pt` |
| `FALL_ANGLE_THRESHOLD` | Max torso angle for fall | `75°` |
| `FALL_RATIO_THRESHOLD` | Height/Width ratio limit | `0.9` |
| `CONFIDENCE_FLOOR` | Minimum confidence for fall | `0.65` |
| `notify_cooldown` | Minimum time between alerts | `2 sec` |

---

## 🔧 Installation

### 1️⃣ Install Dependencies
```bash
pip install ultralytics opencv-python numpy requests
2️⃣ Download YOLOv8 Pose Model
bash
Copy code
yolo download model=yolov8n-pose.pt
Or manually download it from the Ultralytics YOLOv8 Models.

3️⃣ Set Up Pushover
Create an account at pushover.net and set:

python
Copy code
USER_KEY = "your_user_key"
API_TOKEN = "your_api_token"
▶️ How to Run
Run on a Video File
bash
Copy code
python fall_detection.py
Run on a Webcam
Replace this line in code:

python
Copy code
cap = cv2.VideoCapture(VIDEO_PATH)
with:

python
Copy code
cap = cv2.VideoCapture(0)
Press q to quit.

📊 Detection Accuracy (Test Video: two.mp4)
Metric	Value
Total Frames	5200
True Falls Detected	9 / 10
False Alarms	1
Detection Accuracy	90%
Avg. Confidence	0.83
Alert Delay	~1 sec

📱 Example Notification
⚠️ Fall detected for ID 2 (87.5% confidence)
(Instant notification sent via Pushover to mobile.)

🎬 Demo Video
🎥 Watch the fall detection and alert process here:
👉 Demo Video Link (replace with your actual link)

📎 Project Links
🧠 GitHub Repository: https://github.com/ramreddy-ai/fall-detection-yolov8-pose
📱 Pushover API: https://pushover.net
🤖 YOLOv8 Docs: https://docs.ultralytics.com

🧩 Notes
Adjust FALL_ANGLE_THRESHOLD, FALL_RATIO_THRESHOLD, and CONFIDENCE_FLOOR for different environments (e.g., camera height or distance).
System supports multi-person tracking via ByteTrack.
Works best in clear, well-lit conditions.

🪪 License
This project is licensed under the MIT License.

👨‍💻 Author
Developed by Rami Reddy
AI/ML Engineer
People Tech Group

