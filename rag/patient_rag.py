import requests
from query import search_knowledge


API_URL = "http://127.0.0.1:5000"


def get_patient_context(patient_id):

    response = requests.get(
        f"{API_URL}/patient/{patient_id}/context",
        timeout=3
    )

    response.raise_for_status()

    return response.json()


def build_patient_query(context):

    alerts = ", ".join(context.get("alerts", []))

    return (
        f"Patient {context.get('patient_id')} has status "
        f"{context.get('status')}. "
        f"Location: {context.get('location')}. "
        f"Alerts: {alerts}. "
        f"What does this combination of alerts mean?"
    )


if __name__ == "__main__":

    patient_id = "P001"

    print("\nFetching patient context...\n")

    context = get_patient_context(patient_id)

    print("Current Patient Context:")
    print(context)

    query = build_patient_query(context)

    print("\nRAG Query:")
    print(query)

    print("\nRetrieved Medical Knowledge:\n")

    results = search_knowledge(query, k=3)

    for i, result in enumerate(results, 1):

        print(f"--- Knowledge {i} ---")
        print(result["document"])
        print(f"Distance: {result['distance']:.4f}")
        print()
