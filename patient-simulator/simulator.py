import json
import time
from datetime import datetime
from kafka import KafkaProducer


# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def generate_patient_data():
    return {
        "patient_id": "P001",
        "timestamp": datetime.now().isoformat(),
        "heart_rate": 115,
        "spo2": 91,
        "temperature": 38.5,
        "blood_pressure": "145/90",
        "movement": "low",
        "location": "ICU-12"
    }


while True:
    patient_data = generate_patient_data()

    producer.send("patient-data", patient_data)
    producer.flush()

    print("Sent to Kafka:")
    print(json.dumps(patient_data, indent=2))

    time.sleep(5)
