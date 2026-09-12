from flask import Flask, render_template
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000"


@app.route("/")
def dashboard():

    # Get current patient context
    try:
        response = requests.get(
            f"{API_URL}/patient/P001/context",
            timeout=3
        )
        context = response.json()

    except Exception:
        context = {
            "error": "Context API unavailable"
        }

    # Get AI assessment
    try:
        response = requests.get(
            f"{API_URL}/patient/P001/ai-assessment",
            timeout=10
        )
        ai_assessment = response.json()

    except Exception:
        ai_assessment = {
            "error": "AI assessment unavailable"
        }

    return render_template(
        "dashboard.html",
        context=context,
        ai_assessment=ai_assessment
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
