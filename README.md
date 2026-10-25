# AI Based Early Fire Detection System

An autonomous, real-time fire detection and emergency mitigation architecture combining computer vision with hardware automation, developed as part of the 3rd Semester Engineering Clinic Lab at CGC University, Mohali.

## 👥 Team Members (CSE Section D1)
* **Vinit Kumar** (Team Leader) — Roll No: `2456334`
* **Sujal** — Roll No: `2546296`
* **Yatharth Rana** — Roll No: `2546339`
* **Sushant Kumar** — Roll No: `2546308`
* **Faculty Mentor:** Mr. Ujjwal

---

## 🚀 Core Innovations & Features
* **Edge-Computed Vision:** Processes live camera feeds using Python, Flask, and OpenCV with strict HSV color-space chromatic matrices and contour-area thresholding (`>4000`) to eliminate false positives.
* **Asynchronous Telemetry:** Utilizes non-blocking multi-threading (`threading`) to dispatch photographic evidence via the Telegram Bot API without causing video stream latency or freezing.
* **Hardware-Software Bridging:** Employs `PySerial` to communicate instantly with an Arduino Uno microcontroller, triggering physical alarms (piezo buzzers and warning LEDs) within sub-50ms latencies.

---

## 🛠️ Tech Stack
* **Back-End & Vision:** Python, Flask, OpenCV (`cv2`), PySerial
* **Hardware:** Arduino Uno, Breadboard, Piezo Buzzer, USB Optical Webcam
* **Cloud & Messaging:** Telegram Bot REST API
* **Front-End Dashboard:** HTML5, CSS3, JavaScript (Glassmorphic Dark-Mode UI)

---

## ⚙️ Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/ai-fire-detection-system.git](https://github.com/your-username/ai-fire-detection-system.git)
   cd ai-fire-detection-system
