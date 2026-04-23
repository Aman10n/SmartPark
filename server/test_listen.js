const io = require('socket.io-client');
const mqtt = require('mqtt');

const socket = io('http://localhost:3000');
console.log("Connecting to WebSocket...");

socket.on('connect', () => {
    console.log("WebSocket connected!");
});

socket.on('init_state', (state) => {
    console.log("Received 'init_state'");
});

socket.on('alpr_event', (data) => {
    console.log(">>> SUCCESS <<< Received ALPR event via Socket.IO:", data);
});

const client = mqtt.connect('mqtt://127.0.0.1:1883');
client.on('connect', () => {
    console.log("MQTT connected! Subscribing to #...");
    client.subscribe('#');
});

client.on('message', (topic, msg) => {
    console.log("MQTT Received natively:", topic, msg.toString());
});

setTimeout(() => {
    console.log("Test finished.");
    process.exit(0);
}, 5000);
