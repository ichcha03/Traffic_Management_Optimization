# 🚦 AI Based Traffic Flow Optimization System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV-orange)

## 📄 Abstract
**AI Based Traffic Flow Optimization** is an intelligent traffic management system designed to optimize signal timings at intersections using Computer Vision and Traffic Engineering principles. By analyzing real-time traffic density from camera feeds, the system dynamically adjusts signal cycles to minimize congestion and average vehicle waiting time.

This project was developed as a **Semester Project for B.Tech (3rd Year / 5th Sem)** to demonstrate the application of AI in Smart City infrastructure.

---

## ✨ Key Features
*   **Multi-Lane Detection**: Processes images from 4 lanes (North, South, East, West) simultaneously.
*   **Vehicle Classification**: Detects and counts distinct vehicle types (Cars, Motorcycles, Buses, Trucks) using **YOLOv8**.
*   **Smart Density Calculation**: Assigns weighted scores (PCU - Passenger Car Units) to different vehicles (e.g., Bus > Car) for accurate load assessment.
*   **Webster's Method Optimization**: Uses the industry-standard **Webster’s Delay Minimization Algorithm** to calculate scientifically optimal signal cycle lengths.
*   **Dynamic Signal Timing**: Automatically allocates Green, Red, and Yellow times based on real-time traffic demand.
*   **Interactive Dashboard**: User-friendly web interface built with **Streamlit** for visualization and control.

---

## 🛠️ Tech Stack
*   **Language**: Python
*   **Computer Vision**: Ultralytics YOLOv8, OpenCV
*   **Web Framework**: Streamlit
*   **Data Processing**: NumPy
*   **Algorithm**: Webster's Method (Traffic Engineering)

---

## 🧠 Optimization Algorithm: Webster's Method
Unlike simple fixed-timer signals, this system implements **Webster's Method** to minimize total delay.

1.  **Saturation Flow ($S$)**: Assumed max capacity of ~1800 PCU/hr per lane.
2.  **Flow Ratio ($y$)**: Calculated as $\frac{\text{Actual Flow}}{\text{Saturation Flow}}$.
3.  **Optimal Cycle Time ($C_{opt}$)**:
    $$ C_{opt} = \frac{1.5L + 5}{1 - Y} $$
    *   $L$: Total lost time (start-up delays + yellow intervals).
    *   $Y$: Sum of critical flow ratios for the intersection.
4.  **Green Time Allocation**: Distributed proportionally to the flow ratio ($y$) of each lane.

This ensures that the signal cycle expands during peak hours to clear queues and shrinks during off-peak hours to reduce waiting.

---

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.8 or higher
*   Git

### Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Gaurav-Chaudhary04/Traffic_Flow_Optimization.git
    cd Traffic_Flow_Optimization
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download YOLOv8 Weights**
    The system uses `yolov8n.pt`. It will automatically download on the first run, or you can place your custom model in the root directory.

---

## 💻 Usage

1.  **Run the Application**
    ```bash
    streamlit run camera_problems.py
    ```

2.  **Upload Traffic Images**
    *   The interface will ask for 4 images corresponding to North, South, East, and West lanes.
    *   Upload sample images (or capture from camera feeds if integrated).

3.  **View Results**
    *   The system will display annotated images with detected vehicles.
    *   It will show the **Optimized Cycle Time** (e.g., 92s).
    *   It will provide the precise **Green/Red/Yellow** timing split for each lane.

---

## 📂 Project Structure
```
Traffic_Flow_Optimization/
├── camera_problems.py      # Main Streamlit Application (Frontend)
├── vehicle_counter.py      # YOLOv8 Detection Logic (Backend)
├── traffic_optimizer.py    # Webster's Method Implementation (Algorithm)
├── requirements.txt        # Project Dependencies
├── yolov8n.pt              # Pre-trained YOLO Model
└── README.md               # Project Documentation
```

---

## 🔮 Future Scope
*   **Real-Time Video Integration**: Connect directly to CCTV feeds for live processing.
*   **Emergency Vehicle Priority**: Detect ambulances/fire trucks and force green signals.
*   **Multi-Intersection Sync**: Coordinate multiple signals to create "Green Waves".
*   **Edge Deployment**: Optimize for running on Raspberry Pi/Jetson Nano.

---

## 👨‍💻 Author
**Ichcha**
*   B.Tech (3rd Year)
*   [GitHub Profile](https://github.com/ichcha03)
*   [LinkedIn](https://www.linkedin.com/in/ichcha-mehrishi-344478289/)

---
*Built with ❤️ for the Future of Smart Mobility.*
