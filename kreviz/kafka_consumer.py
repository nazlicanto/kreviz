# kreviz/kafka_consumer.py

from kafka import KafkaConsumer
import json

def consume_messages(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',  # Start from the earliest messages
        group_id='chat-group',         # Consumer group ID
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    for message in consumer:
        print("Received message:", message.value)
        # You'll need to send this message to the WebSocket
