import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from agent.agent import agent

from flask import Flask, jsonify
import redis
import json

app = Flask(__name__)

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    return jsonify({
        "service": "Patient Monitoring Context API",
        "status": "running"
    })

@app.route("/patient/<patient_id>/context")
def get_patient_context(patient_id):

    redis_key = f"patient:{patient_id}:context"

    data = redis_client.get(redis_key)

    if data is None:
        return jsonify({
            "error": "Patient context not found"
        }), 404

    return jsonify(json.loads(data))

@app.route("/patient/<patient_id>/history")
def get_patient_history(patient_id):

    import psycopg2

    db = psycopg2.connect(
        host="localhost",
        port=5432,
        database="patient_monitoring",
        user="patient_app",
        password="patient_app_password"
    )

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT timestamp,
               heart_rate,
               spo2,
               temperature,
               blood_pressure,
               movement,
               location,
               status,
               alerts
        FROM patient_vitals
        WHERE patient_id = %s
        ORDER BY id DESC
        LIMIT 20
        """,
        (patient_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    history = []

    for row in rows:
        history.append({
            "timestamp": row[0].isoformat(),
            "heart_rate": row[1],
            "spo2": row[2],
            "temperature": row[3],
            "blood_pressure": row[4],
            "movement": row[5],
            "location": row[6],
            "status": row[7],
            "alerts": json.loads(row[8]) if row[8] else []
        })

    return jsonify({
        "patient_id": patient_id,
        "history": history
    })
@app.route("/patient/<patient_id>/ai-assessment")
def get_ai_assessment(patient_id):

    result = agent.invoke({
        "patient_id": patient_id,
        "patient_context": {},
        "query": "",
        "retrieved_knowledge": [],
        "response": ""
    })

    return jsonify({
        "patient_id": patient_id,
        "assessment": result["response"]
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
