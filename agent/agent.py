import requests
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

import sys
import os


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

from rag.query import search_knowledge


# ============================================================
# API
# ============================================================

API_URL = "http://127.0.0.1:5000"


# ============================================================
# LANGGRAPH STATE
# ============================================================

class AgentState(TypedDict):
    patient_id: str
    patient_context: dict
    history: list
    trend_analysis: dict
    query: str
    retrieved_knowledge: list
    response: str


# ============================================================
# NODE 1
# GET CURRENT PATIENT CONTEXT
# ============================================================

def get_patient_context(state: AgentState):

    patient_id = state["patient_id"]

    response = requests.get(
        f"{API_URL}/patient/{patient_id}/context",
        timeout=5
    )

    response.raise_for_status()

    state["patient_context"] = response.json()

    return state


# ============================================================
# NODE 2
# GET PATIENT HISTORY
# ============================================================

def get_patient_history(state: AgentState):

    patient_id = state["patient_id"]

    response = requests.get(
        f"{API_URL}/patient/{patient_id}/history",
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    state["history"] = data.get("history", [])

    return state


# ============================================================
# NODE 3
# ANALYZE TREND
# ============================================================

def analyze_trend(state: AgentState):

    history = state.get("history", [])

    if not history:

        state["trend_analysis"] = {
            "overall": "NO DATA",
            "heart_rate": "No data",
            "spo2": "No data",
            "temperature": "No data",
            "blood_pressure": "No data"
        }

        return state


    # History API returns newest first
    latest = history[0]
    oldest = history[-1]


    # --------------------------------------------------------
    # Numeric values
    # --------------------------------------------------------

    latest_hr = float(latest.get("heart_rate") or 0)
    oldest_hr = float(oldest.get("heart_rate") or 0)

    latest_spo2 = float(latest.get("spo2") or 0)
    oldest_spo2 = float(oldest.get("spo2") or 0)

    latest_temp = float(latest.get("temperature") or 0)
    oldest_temp = float(oldest.get("temperature") or 0)


    latest_bp = int(
        str(
            latest.get(
                "blood_pressure",
                "0/0"
            )
        ).split("/")[0]
    )

    oldest_bp = int(
        str(
            oldest.get(
                "blood_pressure",
                "0/0"
            )
        ).split("/")[0]
    )


    # --------------------------------------------------------
    # Calculate differences
    # --------------------------------------------------------

    hr_change = latest_hr - oldest_hr
    spo2_change = latest_spo2 - oldest_spo2
    temp_change = latest_temp - oldest_temp
    bp_change = latest_bp - oldest_bp


    # --------------------------------------------------------
    # Determine individual trends
    # --------------------------------------------------------

    if hr_change > 2:
        hr_trend = "Increasing"

    elif hr_change < -2:
        hr_trend = "Decreasing"

    else:
        hr_trend = "Stable"


    if spo2_change > 1:
        spo2_trend = "Improving"

    elif spo2_change < -1:
        spo2_trend = "Worsening"

    else:
        spo2_trend = "Stable"


    if temp_change > 0.2:
        temp_trend = "Increasing"

    elif temp_change < -0.2:
        temp_trend = "Decreasing"

    else:
        temp_trend = "Stable"


    if bp_change > 5:
        bp_trend = "Increasing"

    elif bp_change < -5:
        bp_trend = "Decreasing"

    else:
        bp_trend = "Stable"


    # --------------------------------------------------------
    # Overall trend
    # --------------------------------------------------------

    worsening_count = 0
    improving_count = 0


    if hr_trend == "Increasing":
        worsening_count += 1

    elif hr_trend == "Decreasing":
        improving_count += 1


    if spo2_trend == "Worsening":
        worsening_count += 1

    elif spo2_trend == "Improving":
        improving_count += 1


    if temp_trend == "Increasing":
        worsening_count += 1

    elif temp_trend == "Decreasing":
        improving_count += 1


    if bp_trend == "Increasing":
        worsening_count += 1

    elif bp_trend == "Decreasing":
        improving_count += 1


    if worsening_count > improving_count:

        overall = "WORSENING"

    elif improving_count > worsening_count:

        overall = "IMPROVING"

    else:

        overall = "STABLE"


    # --------------------------------------------------------
    # Save trend result
    # --------------------------------------------------------

    state["trend_analysis"] = {

        "overall": overall,

        "heart_rate": hr_trend,

        "spo2": spo2_trend,

        "temperature": temp_trend,

        "blood_pressure": bp_trend,

        "changes": {
            "heart_rate": hr_change,
            "spo2": spo2_change,
            "temperature": temp_change,
            "blood_pressure": bp_change
        }
    }


    return state


# ============================================================
# NODE 4
# RAG KNOWLEDGE RETRIEVAL
# ============================================================

def retrieve_knowledge(state: AgentState):

    context = state["patient_context"]

    trend = state["trend_analysis"]

    alerts = ", ".join(
        context.get("alerts", [])
    )


    query = (
        f"Patient status: {context.get('status')}. "
        f"Current alerts: {alerts}. "
        f"Heart rate trend: {trend.get('heart_rate')}. "
        f"SpO2 trend: {trend.get('spo2')}. "
        f"Temperature trend: {trend.get('temperature')}. "
        f"Blood pressure trend: {trend.get('blood_pressure')}. "
        f"Overall trend: {trend.get('overall')}. "
        f"Explain the clinical significance of multiple "
        f"abnormal vital signs and persistent trends."
    )


    state["query"] = query


    results = search_knowledge(
        query,
        k=5
    )


    state["retrieved_knowledge"] = [
        result["document"]
        for result in results
    ]


    return state


# ============================================================
# NODE 5
# GENERATE AI RESPONSE
# ============================================================

def generate_response(state: AgentState):

    context = state["patient_context"]

    history = state["history"]

    trend = state["trend_analysis"]

    knowledge = state["retrieved_knowledge"]


    alerts = ", ".join(
        context.get("alerts", [])
    )


    # --------------------------------------------------------
    # Recent history
    # --------------------------------------------------------

    history_lines = []

    for record in history[:5]:

        history_lines.append(
            f"- {record.get('timestamp')}: "
            f"HR={record.get('heart_rate')}, "
            f"SpO2={record.get('spo2')}, "
            f"Temp={record.get('temperature')}, "
            f"BP={record.get('blood_pressure')}, "
            f"Status={record.get('status')}"
        )


    history_text = "\n".join(history_lines)


    # --------------------------------------------------------
    # Final assessment
    # --------------------------------------------------------

    response = (

        f"Patient {context.get('patient_id')} "
        f"is currently in {context.get('status')} status.\n\n"

        f"Location: {context.get('location')}\n"

        f"Current Alerts: {alerts}\n\n"


        f"Recent Patient History:\n"

        f"{history_text}\n\n"


        f"Trend Analysis:\n"

        f"- Overall Trend: {trend.get('overall')}\n"

        f"- Heart Rate: {trend.get('heart_rate')}\n"

        f"- SpO2: {trend.get('spo2')}\n"

        f"- Temperature: {trend.get('temperature')}\n"

        f"- Blood Pressure: {trend.get('blood_pressure')}\n\n"


        f"Assessment:\n"

        f"The system detected multiple abnormal vital-sign "
        f"alerts. Recent patient history and vital-sign trends "
        f"were analyzed to provide additional context. "
        f"The current trend classification is "
        f"{trend.get('overall')}.\n\n"


        f"Relevant Knowledge:\n"

        + "\n".join(
            f"- {item}"
            for item in knowledge[:3]
        )


        + "\n\n"


        f"Note: This automated output is a "
        f"decision-support signal and should not "
        f"be treated as a diagnosis."
    )


    state["response"] = response

    return state


# ============================================================
# CREATE LANGGRAPH
# ============================================================

graph = StateGraph(AgentState)


# ============================================================
# NODES
# ============================================================

graph.add_node(
    "get_patient_context",
    get_patient_context
)

graph.add_node(
    "get_patient_history",
    get_patient_history
)

graph.add_node(
    "analyze_trend",
    analyze_trend
)

graph.add_node(
    "retrieve_knowledge",
    retrieve_knowledge
)

graph.add_node(
    "generate_response",
    generate_response
)


# ============================================================
# EDGES
# ============================================================

graph.add_edge(
    START,
    "get_patient_context"
)

graph.add_edge(
    "get_patient_context",
    "get_patient_history"
)

graph.add_edge(
    "get_patient_history",
    "analyze_trend"
)

graph.add_edge(
    "analyze_trend",
    "retrieve_knowledge"
)

graph.add_edge(
    "retrieve_knowledge",
    "generate_response"
)

graph.add_edge(
    "generate_response",
    END
)


# ============================================================
# COMPILE
# ============================================================

agent = graph.compile()


# ============================================================
# TEST AGENT
# ============================================================

if __name__ == "__main__":

    result = agent.invoke({

        "patient_id": "P001",

        "patient_context": {},

        "history": [],

        "trend_analysis": {},

        "query": "",

        "retrieved_knowledge": [],

        "response": ""
    })


    print()
    print("================================")
    print("       LANGGRAPH AI AGENT")
    print("================================")
    print()

    print(result["response"])
