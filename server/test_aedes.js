const { Aedes } = require('aedes');
const aedes = new Aedes();
const aedesServerFactory = require('aedes-server-factory');
const mqtt = require('mqtt');

const server = aedesServerFactory.createServer(aedes);
aedes.on('publish', (packet, client) => {
    if (packet.topic === 'test_topic') {
        console.log(">>> AEDES NATIVE INTERCEPT WORKS: " + packet.payload.toString());
    }
});

server.listen(1884, '127.0.0.1', () => {
    const client = mqtt.connect('mqtt://127.0.0.1:1884');
    client.on('connect', () => {
        client.publish('test_topic', 'Hello from MQTT Client!', {qos: 0}, () => {
            console.log("Publish ACKed by Broker");
            setTimeout(() => process.exit(0), 200);
        });
    });
    client.on('error', (err) => console.log("Client error:", err));
});
