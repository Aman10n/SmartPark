const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://127.0.0.1:1883');

client.on('connect', () => {
    console.log("Connected, sending ENTRY D01...");
    client.publish('smartpark_unique_demo_12345/parking/alpr', JSON.stringify({
        spot: 'D01',
        direction: 'ENTRY',
        plate: 'TEST 123',
        vehicleType: 'Sedan',
        timestamp: Date.now()
    }), { qos: 0 }, () => {
        console.log("Sent. Closing.");
        client.end();
    });
});
client.on('error', (err) => console.error("Error:", err));
