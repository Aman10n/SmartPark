# SmartPark AI Dashboard

Hey! Welcome to the SmartPark AI Dashboard project. This isn't just a static HTML mockup—it's a fully functional, multi-tier **Edge AI and IoT Smart Parking System**. 

The goal of this project was to simulate a real-world data pipeline where heavy ML inference happens at the edge (using YOLOv8), lightweight battery-powered sensors push state changes, and a Node.js cloud gateway aggregates everything to push live updates to a dashboard via WebSockets.

## 🌟 What's Inside? (Features)

* **Live Edge AI ALPR Simulation:** Built-in ALPR (Automatic License Plate Recognition) engine that generates real-time vehicle entry/exit events with randomized license plates and vehicle types.
* **IoT Ground Sensor Array:** Embedded virtual LoRaWAN ground sensors that continuously publish parking spot occupancy changes across all 48 spots.
* **Dynamic Surge Pricing Engine:** The backend calculates live pricing based on the current capacity of the parking lot automatically. Just like Uber surge pricing, but for parking.
* **Real-time WebSockets:** A Node.js backend acts as our Cloud Gateway, instantly pushing all telemetry events to the frontend UI via Socket.IO without needing page refreshes.
* **Manual Override & Offline Mapping:** A built-in IoT simulation panel in the UI to instantly toggle cameras offline, force surge pricing, or manually trigger vehicle entry/exit events.

## ⚙️ How the Workflow Operates

1. **The Edge AI ALPR Engine (built into `server.js`)**: Simulates camera nodes detecting vehicles. It generates fake license plate reads and pushes ALPR events every 4–8 seconds with randomized vehicle types (Sedan, SUV, Hatchback, etc.).
2. **The IoT Ground Sensors (built into `server.js`)**: Simulates magnetometer-based ground sensors checking for cars above them. Fires random `free`/`occupied` state changes every 2–5 seconds across all 4 zones.
3. **The Gateway Server (`server/server.js`)**: A Node.js Express server that manages the global state of the 48-spot parking facility, runs the dynamic pricing algorithm, and broadcasts all updates to connected dashboard clients using `socket.io`.
4. **The Dashboard (`index.html`)**: The frontend! It connects via WebSocket and paints a modern glassmorphism UI reacting in real-time to the data stream.

---

## 🚀 How to Run It On Your Laptop

Just **one terminal, two commands**. Everything starts together — the server, the IoT sensors, and the ALPR engine all boot up automatically.

**Prerequisites:**
- Have [Node.js](https://nodejs.org/) (v18+) installed.

### Quick Start

```bash
npm install
npm start
```

*➡️ Open your browser and go to `http://localhost:3000`. The dashboard will be live with data flowing within 2 seconds!*

You'll see:
- 🅿️ **Parking Map** lighting up as sensors report spots occupied/free
- 📷 **ALPR Feed** streaming license plate detection events in real-time
- 💰 **Dynamic Pricing** adjusting based on lot utilization
- 📊 **Analytics Charts** displaying occupancy and revenue trends

### IoT Simulation Panel

Navigate to the **IoT Simulation** tab in the sidebar to manually:
- Trigger a **Vehicle ENTRY** event (or press `E`)
- Trigger a **Vehicle EXIT** event (or press `X`)
- **Force Peak Surge Pricing** to test the pricing engine
- **Toggle Camera Disconnect** to simulate hardware failure

---

## 🌐 Live Deployment

This project is deployed on **Render** and runs with a single `npm start` command.

**Deploy your own:**
1. Fork this repo
2. Go to [render.com](https://render.com) → New Web Service → Connect your fork
3. Set Build Command: `npm install` | Start Command: `npm start` | Instance: Free
4. Done! Live in ~2 minutes.

---

## 📁 Project Structure

```
SmartPark/
├── index.html              # Dashboard frontend (glassmorphism UI)
├── css/style.css           # Styling (dark theme, animations)
├── js/app.js               # Frontend logic (WebSocket client, Chart.js)
├── server/
│   └── server.js           # Gateway server + built-in simulators
├── edge-ai/                # Standalone YOLOv8 ALPR script (optional)
│   ├── main.py             #   Can run separately against real camera feeds
│   └── requirements.txt
├── iot-sensors/            # Standalone IoT sensor script (optional)
│   ├── virtual_sensors.py  #   Can run separately for external testing
│   └── requirements.txt
├── package.json            # Node.js dependencies & start script
└── .gitignore
```

> **Note:** The `edge-ai/` and `iot-sensors/` Python scripts are optional standalone versions. They can be pointed at any running SmartPark server (local or deployed) to push external telemetry data via REST APIs (`POST /api/alpr` and `POST /api/spots`).

---

## 🔧 Real-World Hardware (For Production)

To move from simulation to a real parking facility, you would need:

| Component | Hardware | Per Unit |
|-----------|----------|----------|
| Ground Sensors | ESP32 + Magnetometer (BMM150) | ~$20 |
| ALPR Camera | Raspberry Pi 5 + USB Camera + YOLOv8 | ~$100 |
| Local Gateway | Raspberry Pi 4 running `server.js` | ~$60 |
| Wireless | LoRa Gateway or WiFi Router | ~$80 |

**Estimated total for 48 spots: ~$1,500**

---

Feel free to fork, break, and rebuild it!
