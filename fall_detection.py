import cv2
import numpy as np
import time
from ultralytics import YOLO
import requests

# --- 1. CONFIGURATION ---
VIDEO_PATH = '/home/aiml/fall/two.mp4'
MODEL_NAME = 'yolov8n-pose.pt'

FALL_ANGLE_THRESHOLD = 75.0    # Torso tilt threshold (deg)
FALL_RATIO_THRESHOLD = 0.9     # Height/Width ratio threshold
CONFIDENCE_FLOOR = 0.65        # Fall confidence threshold

LEFT_SHOULDER_IDX, RIGHT_SHOULDER_IDX = 5, 6
LEFT_HIP_IDX, RIGHT_HIP_IDX = 11, 12

# --- 2. Pushover Setup ---
USER_KEY = 'u7wv7trxbf77hcksf51yrnfp9y12uj'
API_TOKEN = 'a84rxnpuy5jr8jr2d2tik4z2fts8of'

def send_fall_notification(message: str):
    """Send fall alert via Pushover."""
    url = "https://api.pushover.net:443/1/messages.json"
    data = {"token": API_TOKEN, "user": USER_KEY, "message": message}
    try:
        response = requests.post(url, data=data, timeout=5)
        if response.status_code == 200:
            print(f"[NOTIFY] {message}")
        else:
            print(f"[WARN] Notification failed: {response.status_code} {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to send notification: {e}")

# --- 3. Helper Functions ---
def calculate_torso_angle(kpts_xyc: np.ndarray) -> float:
    """Calculate torso angle (vertical = 0°, horizontal = 90°)."""
    l_sh, r_sh = kpts_xyc[LEFT_SHOULDER_IDX, :2], kpts_xyc[RIGHT_SHOULDER_IDX, :2]
    l_hip, r_hip = kpts_xyc[LEFT_HIP_IDX, :2], kpts_xyc[RIGHT_HIP_IDX, :2]

    mid_shoulder = (l_sh + r_sh) / 2
    mid_hip = (l_hip + r_hip) / 2
    vec = mid_shoulder - mid_hip

    angle_rad = np.arctan2(vec[0], -vec[1])
    torso_angle = abs(np.degrees(angle_rad))
    return min(90.0, torso_angle)

def calculate_fall_confidence(kpts_xyc: np.ndarray, box_xyxy: np.ndarray) -> tuple[bool, float]:
    """Compute fall likelihood based on pose geometry."""
    torso_angle = calculate_torso_angle(kpts_xyc)
    score_angle = 1.0 - (torso_angle / 90.0)

    h, w = box_xyxy[3] - box_xyxy[1], box_xyxy[2] - box_xyxy[0]
    aspect_ratio = h / max(w, 1e-6)
    score_ratio = np.clip((3.0 - aspect_ratio) / 2.0, 0.0, 1.0)

    torso_kpt_indices = [LEFT_SHOULDER_IDX, RIGHT_SHOULDER_IDX, LEFT_HIP_IDX, RIGHT_HIP_IDX]
    avg_kpt_conf = np.mean(kpts_xyc[torso_kpt_indices, 2])

    W_KPT, W_RATIO, W_ANGLE = 0.3, 0.35, 0.35
    FDC = (W_KPT * avg_kpt_conf) + (W_RATIO * score_ratio) + (W_ANGLE * score_angle)

    is_fall = (torso_angle < FALL_ANGLE_THRESHOLD) and (aspect_ratio < FALL_RATIO_THRESHOLD) and (FDC > CONFIDENCE_FLOOR)
    return is_fall, FDC

# --- 4. MAIN ---
def main():
    try:
        model = YOLO(MODEL_NAME)
        cap = cv2.VideoCapture(VIDEO_PATH)
    except Exception as e:
        print(f"[ERROR] Loading failed: {e}")
        return

    print(f"▶ Processing video: {VIDEO_PATH}")
    last_notify_time = 0
    notify_cooldown = 1  # seconds  <-- reduced cooldown

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)

        if results and results[0].keypoints is not None:
            boxes = results[0].boxes
            keypoints = results[0].keypoints

            for box, kpt in zip(boxes, keypoints):
                if kpt is None or len(kpt.data[0]) < 13:  # Ensure valid keypoints
                    continue

                box_xyxy = box.xyxy.cpu().numpy()[0]
                kpts_xyc = kpt.data.cpu().numpy()[0]
                person_id = int(box.id.item()) if box.id is not None else -1

                is_fall, FDC = calculate_fall_confidence(kpts_xyc, box_xyxy)
                FDC_percent = FDC * 100
                x1, y1, x2, y2 = map(int, box_xyxy)
                label = f"ID {person_id}: {'FALL' if is_fall else 'OK'} ({FDC_percent:.1f}%)"
                color = (0, 0, 255) if is_fall else (0, 255, 0)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, max(30, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                # --- Send notification every 2 sec if still falling ---
                if is_fall and (time.time() - last_notify_time > notify_cooldown):
                    send_fall_notification(f"⚠️ Fall detected for ID {person_id} ({FDC_percent:.1f}% confidence)")
                    last_notify_time = time.time()

        # Resize for better display
        frame_small = cv2.resize(frame, (960, 540))
        cv2.imshow("Fall Detection", frame_small)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Processing complete.")

# --- 5. ENTRY POINT ---
if __name__ == "__main__":
    main()
