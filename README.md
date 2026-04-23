# SmartPark AI Dashboard

Hey! Welcome to the SmartPark AI Dashboard project. This isn't just a static HTML mockup—it's a fully functional, multi-tier **Edge AI and IoT Smart Parking System**. 

The goal of this project was to simulate a real-world data pipeline where heavy ML inference happens at the edge (using YOLOv8), lightweight battery-powered sensors push state changes, and a Node.js cloud gateway aggregates everything to push live updates to a dashboard via WebSockets.

## 🌟 What's Inside? (Features)

* **Live Edge AI Inference:** A Python script running actual computer vision (YOLOv8) to count cars on a video feed and generate ALPR (Automatic License Plate Recognition) events. 
* **IoT Ground Sensor Array:** Another Python simulator representing hundreds of localized LoRaWAN ground sensors that publish parking spot occupancy over HTTP.
* **Dynamic Surge Pricing Engine:** The backend calculates live pricing based on the current capacity of the parking lot automatically. Just like Uber surge pricing, but for parking.
* **Real-time WebSockets:** A Node.js backend acts as our Cloud Gateway, instantly bridging all incoming REST telemetry from the edge devices to the frontend UI without needing page refreshes.
* **Manual Override & Offline Mapping:** A built-in IoT simulation panel in the UI to instantly toggle cameras offline or force manual vehicle flows.

## ⚙️ How the Workflow Operates

1. **The Edge AI (`edge-ai/main.py`)**: This acts as our camera node. It downloads a frame, runs a tensor calculus model (YOLOv8) to detect vehicles, fakes a license plate read for those vehicles, and pushes a lightweight JSON payload to our backend REST API.
2. **The IoT Sensors (`iot-sensors/virtual_sensors.py`)**: This mimics ground sensors checking for cars above them. It wakes up randomly to send binary `free`/`occupied` states directly to the Gateway server.
3. **The Gateway Server (`server/server.js`)**: A Node.js Express server that catches the incoming ALPR webhooks and sensor events. It processes the pricing algorithms, manages the global state of the parking facility, and blasts the updates out to all connected Web UI clients using `socket.io`.
4. **The Dashboard (`index.html`)**: The frontend! It connects via WebSocket to `localhost:3000` and paints a modern glassmorphism UI reacting in real-time to the data stream.

---

## 🚀 How to Run It On Your Laptop

If you downloaded the ZIP or cloned the repo, here are the step-by-step instructions. **You will need 3 separate terminal windows open at the same time** because the backend, the AI camera, and the sensors all run concurrently.

**Prerequisites:**
- Have Node.js installed.
- Have Python 3.8+ installed (with `pip`).

### Terminal 1: Boot the Gateway Server
This starts the backend and the dashboard UI. Start here!

```bash
cd server
npm install
node server.js
```
*➡️ Open your browser and go to `http://localhost:3000`. You'll see the empty dashboard waiting for data.*

### Terminal 2: Start the IoT Sensor Array
Open a new terminal window in the project folder. This boots up the virtual ground sensors.

```bash
cd iot-sensors
pip install -r requirements.txt
python virtual_sensors.py
```
*➡️ Go look at your dashboard! You'll literally see the parking map light up as "sensors" connect and report their spots as occupied or free.*

### Terminal 3: Start the Edge AI NPU (YOLOv8)
Open a third terminal window. This runs the heavy ML stuff.

```bash
cd edge-ai
pip install -r requirements.txt
python main.py
```
*(Note: It will download a ~3MB YOLO model file the very first time you run it).*

*➡️ Watch the terminal as YOLO detects cars, then look at your dashboard's ALPR feed tab to see the license plate data stream in live!*

---

Feel free to fork, break, and rebuild it!
