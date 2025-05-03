import os
import cv2
import torch
import serial
import time
import numpy as np
from ultralytics import YOLO

try:
    from picamera2 import Picamera2
except ImportError:
    print("Error: 'picamera2' module not found. Install it using:")
    print("sudo apt install python3-picamera2")
    exit(1)

# === CONFIG ===
MODEL_PATH = "best.pt"
SERIAL_PORT = "/dev/ttyACM0"   # Update if your Arduino is on a different port
BAUD_RATE = 9600
CLASS_TO_COMMAND = {
    'nut': 'A',
    'bolt': 'B',
    'washer': 'C',
    'defected_nut': 'D',
    'defected_bolt': 'D',
    'defected_washer': 'D'
}
CONF_THRESHOLD = 0.5
OUTPUT_DIR = "./output"

# === SETUP SERIAL ===
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset
    print("Serial connected to Arduino.")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    arduino = None

def setup_camera():
    try:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={"size": (640, 480)})
        picam2.configure(config)
        picam2.start()
        return picam2
    except Exception as e:
        print(f"Camera error: {e}")
        exit(1)

def detect_from_camera(model):
    picam2 = setup_camera()
    print("Press 'q' to exit detection...")

    while True:
        try:
            frame = picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = model(frame, conf=CONF_THRESHOLD, iou=0.5, verbose=False)[0]

            boxes = results.boxes.xyxy.cpu().numpy()
            confs = results.boxes.conf.cpu().numpy()
            cls_ids = results.boxes.cls.cpu().numpy().astype(int)
            class_names = model.names

            if len(confs) > 0:
                top_idx = int(np.argmax(confs))
                class_name = class_names[cls_ids[top_idx]]

                print(f"Detected: {class_name} ({confs[top_idx]:.2f})")

                # Send command to Arduino
                if class_name in CLASS_TO_COMMAND and arduino:
                    command = CLASS_TO_COMMAND[class_name]
                    print(f"Sending command '{command}' to Arduino")
                    arduino.write(command.encode())
                    time.sleep(1)  # Wait between commands

            # Annotate frame
            for box, conf, cls_id in zip(boxes, confs, cls_ids):
                x1, y1, x2, y2 = map(int, box)
                label = f"{class_names[cls_id]}: {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            cv2.imshow("YOLOv8 Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"Error during detection: {e}")
            break

    print("Stopping...")
    picam2.stop()
    cv2.destroyAllWindows()

def main():
    print("Loading model...")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Failed to load YOLO model: {e}")
        return

    detect_from_camera(model)

if __name__ == "__main__":
    main()
