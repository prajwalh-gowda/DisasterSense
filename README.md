# DisasterSense

AI-powered real-time flood monitoring and disaster prediction system using IoT sensors, Machine Learning, Flask backend, and React dashboard.

---

## Problem Statement

Urban floods cause major damage due to lack of real-time monitoring and early warning systems.
DisasterSense predicts flood risk using live environmental sensor data and visualizes alerts through an interactive dashboard.

---

## Features

* Real-time sensor monitoring
* AI-based flood prediction
* Live dashboard visualization
* ESP32 hardware integration
* Emergency risk alerts
* Weather & environmental analytics
* Urban disaster management support

---

## System Architecture

![Architecture](images/architecture.png)

---

## Dashboard Preview

![Dashboard](images/dashboard.png)

---

## Tech Stack

* React.js
* Flask
* Python
* Machine Learning
* ESP32
* REST API
* Leaflet Maps

---

## Workflow

ESP32 Sensors → Python Script → Flask Backend → ML Prediction → React Dashboard

---

## Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd floodsense-dashboard
npm install
npm start
```

### Sensor Simulator

```bash
cd simulator
python sensor_simulator.py
```

---

## Future Improvements

* SMS emergency alerts
* Government integration
* Satellite weather APIs
* Multi-city deployment
* Mobile application support

---

## Team

Developed for Hackathon Project Submission.
