import cv2
import json
import random
import time
import urllib.request
import numpy as np

# Configuration
URL_ALPR = "http://127.0.0.1:3000/api/alpr"

print("==================================================")
print("🧠 Edge AI: YOLOv8 ALPR Inference Engine Starting...")
print("==================================================")

try:
    from ultralytics import YOLO
    print("✅ ultralytics installed. Loading YOLOv8n model...")
    model = YOLO("yolov8n.pt") # Auto-downloads tiny weights (3MB)
except Exception as e:
    print("❌ Could not load ultralytics YOLO model. Please run: pip install ultralytics")
    exit(1)

# REST Setup
print("📡 Connecting to SmartPark REST Gateway at http://127.0.0.1:3000...")

# Helper function to generate fake plate (since we didn't train a custom LPRNet)
def extract_ocr_fake():
    letters = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    digits = '0123456789'
    return f"{random.choice(letters)}{random.choice(letters)} {random.choice(digits)}{random.choice(digits)} {random.choice(letters)}{random.choice(letters)} {random.randint(1000, 9999)}"

print("🚀 Simulating Edge-to-Cloud ALPR Event Stream...")
try:
    while True:
        # Download a sample traffic image to run inference on
        IMAGE_URL = "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=800&q=80"
        print("📸 Fetching sample camera frame for inference...")
        try:
            req = urllib.request.urlopen(IMAGE_URL)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            frame = cv2.imdecode(arr, -1)
            print("✅ Frame captured. Running Neural Network Inference...")
        except Exception as e:
            print(f"❌ Failed to download camera frame: {e}")
            time.sleep(5)
            continue

        # Run actual YOLOv8 inference
        results = model(frame, verbose=False)
        detections = results[0].boxes

        # Filter for 'car' class (class ID 2 in COCO dataset)
        cars = [box for box in detections if int(box.cls[0]) == 2]

        print(f"\n🎯 [YOLOv8 Inference Result] Detected {len(cars)} vehicles in frame.")

        for i, car in enumerate(cars):
            # We pretend we read a plate from the cropped bounding box of each car
            plate = extract_ocr_fake()
            
            # Pick a random spot for the simulation
            spot = f"{random.choice(['A','B','C','D'])}{str(random.randint(1, 12)).zfill(2)}"
            direction = random.choice(["ENTRY", "EXIT"])
            
            payload = {
                "spot": spot,
                "direction": direction,
                "plate": plate,
                "vehicleType": "Sedan", # YOLO detected it's a car
                "timestamp": int(time.time() * 1000)
            }
            
            # Parse bounding box mathematically
            x1, y1, x2, y2 = car.xyxy[0].tolist()
            
            print(f"📷 Cropped BBox: [X:{int(x1)} Y:{int(y1)} W:{int(x2-x1)} H:{int(y2-y1)}] -> OCR Text: {plate}")
            
            req = urllib.request.Request(URL_ALPR, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            try:
                urllib.request.urlopen(req)
                print(f"📤 Published ALPR Event via REST: {direction} -> {plate}")
            except Exception as e:
                print(f"❌ Error sending ALPR event: {e}")
            
            time.sleep(random.uniform(1.5, 3.5))
            
        print("\n✅ Edge Processing complete for this frame. Waiting before next frame...")
        time.sleep(2)

    
except KeyboardInterrupt:
    print("\n⏹️ Edge Node shutting down.")
