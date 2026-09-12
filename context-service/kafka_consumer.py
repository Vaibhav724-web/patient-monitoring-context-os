import json
import redis
import psycopg2
from kafka import KafkaConsumer


# -----------------------------
# Redis Connection
# -----------------------------
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


# -----------------------------
# PostgreSQL Connection
# -----------------------------
db_connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="patient_monitoring",
    user="patient_app",
    password="patient_app_password"
)

db_cursor = db_connection.cursor()


# -----------------------------
# Analyze Patient Data
# -----------------------------
def analyze_patient(patient):
    alerts = []

    if patient["heart_rate"] > 100:
        alerts.append("High heart rate")

    if patient["spo2"] < 94:
        alerts.append("Low SpO2")

    if patient["temperature"] > 38:
        alerts.append("High temperature")

    systolic = int(patient["blood_pressure"].split("/")[0])

    if systolic >= 140:
        alerts.append("High blood pressure")

    if alerts:
        status = "ALERT"
    else:
        status = "STABLE"

    return {
        "patient_id": patient["patient_id"],
        "timestamp": patient.get("timestamp"),
        "location": patient["location"],
        "status": status,
        "alerts": alerts
    }


# -----------------------------
# Kafka Consumer
# -----------------------------

def safe_json_deserializer(data):
    try:
        return json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Skipping invalid Kafka message")
        return None
consumer = KafkaConsumer(
    "patient-vitals",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="context-engine",
    value_deserializer=safe_json_deserializer
)


print("Context Engine started...")
print("Connected to Redis...")
print("Connected to PostgreSQL...")
print("Waiting for patient data...\n")


# -----------------------------
# Process Patient Data
# -----------------------------
for message in consumer:

    patient_data = message.value

    if patient_data is None:
        print("Skipping invalid Kafka message")
        continue
    
    if "timestamp" not in patient_data:
        print("Skipping invalid message: timestamp missing")
        continue

    # Analyze patient data
    context = analyze_patient(patient_data)


    # -------------------------
    # Save latest context to Redis
    # -------------------------
    redis_key = f"patient:{patient_data['patient_id']}:context"

    redis_client.set(
        redis_key,
        json.dumps(context)
    )


    # -------------------------
    # Save history to PostgreSQL
    # -------------------------
    db_cursor.execute(
        """
        INSERT INTO patient_vitals (
            patient_id,
            timestamp,
            heart_rate,
            spo2,
            temperature,
            blood_pressure,
            movement,
            location,
            status,
            alerts
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            patient_data["patient_id"],
            patient_data.get("timestamp"),
            patient_data["heart_rate"],
            patient_data["spo2"],
            patient_data["temperature"],
            patient_data["blood_pressure"],
            patient_data["movement"],
            patient_data["location"],
            context["status"],
            json.dumps(context["alerts"])
        )
    )

    db_connection.commit()


    # -------------------------
    # Display result
    # -------------------------
    print("Patient Context:")
    print(json.dumps(context, indent=2))

    print("Saved to Redis:")
    print(redis_key)

    print("Saved to PostgreSQL: patient_vitals")

    print("-" * 50)
