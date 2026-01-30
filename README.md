# Driver Distraction Detection

A Python application that detects distracted driving in real time using computer vision models and facial behavior analysis.

---

## 🚗 Project Overview

Driving while distracted is a major cause of road accidents. This project monitors a driver’s state using webcam input and alerts when unsafe behavior is detected — such as looking away, closing eyes, or using a phone. It also logs distraction events with timestamps and stores them in a database for later review.

---

## 🧠 Key Features

- 👀 **Head movement tracking** (left/right/up/down)  
- 😴 **Eye closure detection**  
- 📱 **Phone detection using YOLO object recognition**  
- 📝 **Event logging** (SQLite database + text logs)  
- 📸 **Capture snapshot** when distraction is detected  
- 🔐 **Simple admin interface** to review logged events

---

## 🛠️ How It Works

At its core, the system:

1. Uses the **Mediapipe face tracking model** to estimate head pose and eye state.
2. Applies a YOLOv8 model to detect if the driver is holding or using a phone.
3. If distraction is detected:
   - A snapshot of the frame is saved.
   - The event type and timestamp are logged in both a text file and SQLite database.
4. An admin GUI lets you view distraction logs for all drivers.

---

## 📁 Repository Structure

.
├── models/ # Pretrained models (YOLO, etc.)
├── db_manager.py # Database helper functions
├── ddd_core.py # Core detection logic
├── gui_login.py # Login interface for admin
├── gui_main.py # Main admin dashboard
├── haarcascade_frontalface_default.xml # Face detection data
└── README.md


---

## ⚙️ Setup & Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/orianbek/driver_distraction_project.git

2. Create a virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
6. Make sure your webcam is connected and accessible.

📸 Examples

Screenshots and images LATER
