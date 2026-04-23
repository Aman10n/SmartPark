import time
import json
import random
import urllib.request

# Configuration
URL_SPOTS = "http://127.0.0.1:3000/api/spots"

# Virtual Map: 4 zones, 12 spots each
ZONES = ['A', 'B', 'C', 'D']
SPOTS = [f"{z}{str(i).zfill(2)}" for z in ZONES for i in range(1, 13)]

print("🔋 IoT Virtual Sensors Initialized (Simulating LoRaWAN)")

def simulate_sensor_event():
    spot = random.choice(SPOTS)
    # 60% chance to be occupied
    status = "occupied" if random.random() < 0.6 else "free"
    
    payload = {
        "spot": spot,
        "status": status,
        "battery": round(random.uniform(85.0, 99.9), 1),
        "timestamp": int(time.time() * 1000)
    }
    
    req = urllib.request.Request(URL_SPOTS, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
        print(f"📡 [IoT Sensor {spot}] -> {status.upper()} (Bat: {payload['battery']}%)")
    except Exception as e:
        print(f"❌ Error sending IoT event: {e}")

print("▶️ Starting massive virtual sensor deployment...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        # A random sensor wakes up and transmits every 2-5 seconds
        simulate_sensor_event()
        time.sleep(random.uniform(2.0, 5.0))
except KeyboardInterrupt:
    print("\n⏹️ Shutting down virtual sensors.")
