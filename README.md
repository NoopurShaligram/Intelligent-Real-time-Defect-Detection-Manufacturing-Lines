# Intelligent-Real-time-Defect-Detection-Manufacturing-Lines
A real-time object detection system for defect identification in manufacturing lines, leveraging YOLOv8n and Raspberry Pi for automated sorting of defective components.
# 🔧 Intelligent Object Sorting Conveyor System

This project implements an automated conveyor belt system using **Raspberry Pi 5**, **YOLOv8 object detection**, and **Arduino Uno** for actuation. The system identifies components (nut, bolt, washer) and their defective counterparts using a camera and AI, then sorts them into designated bins using a servo-controlled diverter.

## 🎯 Features

- Real-time object detection using **YOLOv8n**
- Image augmentation and custom dataset training
- Automated sorting mechanism via servo motor
- Raspberry Pi camera integration
- Serial communication between Raspberry Pi and Arduino
- Handles 6 classes:
  - `nut`
  - `bolt`
  - `washer`
  - `defected_nut`
  - `defected_bolt`
  - `defected_washer`

---

## 🖥 Hardware Used

- Raspberry Pi 5 + Camera Module 3
- Arduino Uno
- Servo Motor (SG90 or MG996R)
- DC Motor (via HW-130 driver)
- Conveyor belt structure
- Wires, resistors, jumper cables, and power supply

---

## 🧠 Software Stack

- [Python 3.x](https://www.python.org/)
- [YOLOv8 (Ultralytics)](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [Picamera2](https://github.com/raspberrypi/picamera2)
- [Albumentations](https://albumentations.ai/)
- [Arduino IDE](https://www.arduino.cc/en/software)

---

## 📂 Project Structure

```plaintext
.
├── train.py                  # Trains YOLOv8 on custom dataset
├── main.py      # Live detection and Arduino serial communication
├── arduino_sort.ino         # Arduino logic for servo and DC motor control
├── dataset/
│   ├── data.yaml            # YOLO dataset config
│   ├── images/              # Raw and augmented training images
│   └── labels/              # YOLO format labels
├── augmented_images/        # Augmented image output
├── output/                  # YOLO training output
└── README.md                # You're here!
