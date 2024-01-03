# kreviz/kafkaes.py

from kafka import KafkaProducer
import json

def get_kafkaproducer():
    global producer
    if not producer:
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    return producer

def send_message(topic, message):
    try:
        producer = get_kafkaproducer()
        producer.send(topic, message)
        producer.flush()
    except Exception as e:
        print(f"Error in Kafka producer: {e}")





