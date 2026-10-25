# AI Based Early Fire Detection System

An autonomous, real-time fire detection and emergency mitigation architecture combining computer vision with hardware automation, developed as part of the 3rd Semester Engineering Clinic Lab at CGC University, Mohali.

## 👥 Team Members (CSE Section D1)
* **Vinit Kumar** (Team Leader) — Roll No: `2456334`[cite: 6, 7]
* **Sujal** — Roll No: `2546296`[cite: 6, 7]
* **Yatharth Rana** — Roll No: `2546339`[cite: 6, 7]
* **Sushant Kumar** — Roll No: `2546308`[cite: 6, 7]
* **Faculty Mentor:** Mr. Ujjwal[cite: 6, 7]

---

## 🚀 Core Innovations & Features
* **Edge-Computed Vision:** Processes live camera feeds using Python, Flask, and OpenCV with strict HSV color-space chromatic matrices and contour-area thresholding (`>4000`) to eliminate false positives[cite: 6, 7].
* **Asynchronous Telemetry:** Utilizes non-blocking multi-threading (`threading`) to dispatch photographic evidence via the Telegram Bot API without causing video stream latency or freezing[cite: 6, 7].
* **Hardware-Software Bridging:** Employs `PySerial` to communicate instantly with an Arduino Uno microcontroller, triggering physical alarms (piezo buzzers and warning LEDs) within sub-50ms latencies[cite: 6, 7].

---

## 🛠️ Tech Stack
* **Back-End & Vision:** Python, Flask, OpenCV (`cv2`), PySerial[cite: 6, 7]
* **Hardware:** Arduino Uno, Breadboard, Piezo Buzzer, USB Optical Webcam[cite: 6, 7]
* **Cloud & Messaging:** Telegram Bot REST API[cite: 6, 7]
* **Front-End Dashboard:** HTML5, CSS3, JavaScript (Glassmorphic Dark-Mode UI)[cite: 6, 7]

---

## ⚙️ Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/ai-fire-detection-system.git](https://github.com/your-username/ai-fire-detection-system.git)
   cd ai-fire-detection-system
