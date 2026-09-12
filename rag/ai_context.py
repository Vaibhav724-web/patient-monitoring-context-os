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


def create_ai_context(patient_id):

    context = get_patient_context(patient_id)

    alerts = ", ".join(context.get("alerts", []))

    query = (
        f"Patient has {context.get('status')} status. "
        f"Alerts include {alerts}. "
        f"Explain multiple abnormal vital signs and "
        f"why closer clinical attention may be required."
    )

    knowledge = search_knowledge(query, k=5)

    retrieved_text = []

    for result in knowledge:
        retrieved_text.append(result["document"])

    return {
        "patient": context,
        "query": query,
        "retrieved_knowledge": retrieved_text
    }


if __name__ == "__main__":

    result = create_ai_context("P001")

    print("\n===== PATIENT CONTEXT =====")
    print(result["patient"])

    print("\n===== RAG QUERY =====")
    print(result["query"])

    print("\n===== RETRIEVED KNOWLEDGE =====")

    for i, knowledge in enumerate(
        result["retrieved_knowledge"], 1
    ):
        print(f"\n--- Knowledge {i} ---")
        print(knowledge)

    print("\n===== AI CONTEXT READY =====")
