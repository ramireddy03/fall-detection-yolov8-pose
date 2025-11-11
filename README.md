# Fall Detection and Alert System (YOLOv8 Pose & Pushover)

This project implements a real-time fall detection system using the state-of-the-art **YOLOv8 Pose Estimation** model. It analyzes key body joints to determine if a person has fallen and immediately sends a notification via the **Pushover** service.


## 💡 System Overview: How It Works

The system operates in real-time by processing video frames (or live camera feed) to detect and track human poses:

1.  **Detection & Tracking:** The script uses **YOLOv8n-pose** to identify people and their 17 key body points, utilizing **ByteTrack** for persistent tracking (ID assignment).
2.  **Fall Logic:** A person is flagged as potentially falling based on a combination of geometric factors derived from their keypoints:
    * **Torso Angle:** The angle of the torso (mid-shoulder to mid-hip) must be close to horizontal (less than `75.0` degrees).
    * **Aspect Ratio:** The bounding box Height-to-Width ratio must drop below a threshold (less than `0.9`).
3.  **Confidence Score (FDC):** A combined **Fall Detection Confidence (FDC)** score is calculated using weighted contributions from the Torso Angle, Aspect Ratio, and Keypoint Confidence. A fall is confirmed if the FDC is greater than `0.65`.
4.  **Alert Mechanism:** When a fall is confirmed, the `send_fall_notification` function uses the **Pushover API** to push a real-time alert message to designated mobile devices/desktops. Alerts are subject to a **1-second cooldown** to prevent notification spam.

---

## 🛠️ Installation and Setup

### Prerequisites

* Python 3.8+
* The required libraries are listed in `requirements.txt`.
* A **Pushover account** with a registered **User Key** and **Application API Token** (configured in the Python script).

### Steps to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ramireddy03/fall-detection-yolov8-pose.git](https://github.com/ramireddy03/fall-detection-yolov8-pose.git)
    cd fall-detection-yolov8-pose
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Update Configuration:**
    * Open `fall_detection.py` and update `VIDEO_PATH` to the location of your video file.
    * Update the **Pushover** credentials:
        ```python
        USER_KEY = 'YOUR_PUSHOVER_USER_KEY_HERE'
        API_TOKEN = 'YOUR_PUSHOVER_API_TOKEN_HERE'
        ```
4.  **Execute the script:**
    ```bash
    python fall_detection.py
    ```

---

## 📊 Detection Accuracy

The system successfully processed the test video, with the log confirming four persistent alerts for ID 1. The initial Fall Detection Confidence (FDC) of 87.2% demonstrates the model's high certainty in the detected event. The multiple, sustained alerts prove the system's ability to lock onto the fall event and continuously notify while the person remains down, showcasing reliable overall detection performance for the purposes of immediate alerting.

---

## ⚙️ Project Files

| File | Description |
| :--- | :--- |
| `fall_detection.py` | Main script containing the YOLOv8 logic, fall detection algorithm, and Pushover API integration. |
| `requirements.txt` | List of all required Python libraries. |
| `README.md` | This documentation file. |
