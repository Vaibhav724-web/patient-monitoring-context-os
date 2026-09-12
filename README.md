# Patient Monitoring Context OS

## 1. Project Overview

**Patient Monitoring Context OS** is an AI-powered patient monitoring system designed to collect, process, store, analyze, and interpret real-time patient health data.

The system combines **Kafka, Context Processing, Databases, Neo4j, RAG with FAISS, LangGraph AI, REST APIs, and a Doctor Dashboard** to provide meaningful patient context and intelligent clinical insights.

The complete workflow is:

```text
Patient Simulator
       ↓
     Kafka
       ↓
 Context Service
       ↓
 Database / Neo4j
       ↓
   RAG + FAISS
       ↓
 LangGraph AI Agent
       ↓
    REST API
       ↓
 Doctor Dashboard
```

---

## 2. Problem Statement

Traditional patient monitoring systems mainly display individual vital signs such as heart rate, SpO2, temperature, and blood pressure.

However, healthcare professionals need more than individual values. They need **context**, including:

* Current patient condition
* Historical patient information
* Trends in vital signs
* Abnormal conditions
* Relevant medical knowledge
* AI-assisted interpretation

The proposed system addresses this problem by integrating real-time patient data with contextual processing, knowledge retrieval, and AI-based reasoning.

---

## 3. Objectives

The main objectives of the project are:

1. Generate realistic patient monitoring data.
2. Stream patient data using Apache Kafka.
3. Process incoming patient information using a context service.
4. Store patient information for later analysis.
5. Represent patient relationships and context using Neo4j.
6. Build a medical knowledge base.
7. Implement RAG using FAISS.
8. Use LangGraph for AI-based patient analysis.
9. Provide REST APIs for accessing patient information and AI results.
10. Provide a doctor-friendly dashboard.
11. Identify abnormal patient conditions.
12. Analyze patient vital trends.
13. Provide contextual AI-assisted insights to healthcare professionals.

---

## 4. Existing Solutions

Existing patient monitoring solutions include:

* ICU monitoring systems
* Hospital Information Systems
* Electronic Health Record systems
* Remote Patient Monitoring systems
* Wearable health monitoring systems
* IoT-based healthcare systems

These systems are useful for collecting and displaying patient information. However, many systems focus mainly on individual measurements and dashboards rather than combining **real-time streaming, contextual patient information, medical knowledge retrieval, and AI reasoning** in a single pipeline.

### Research Gap

The proposed system addresses this gap by combining:

```text
Real-time Data
      +
Context Processing
      +
Historical Information
      +
Medical Knowledge
      +
RAG
      +
AI Reasoning
      =
Context-Aware Patient Monitoring
```

---

## 5. Proposed System

The proposed Patient Monitoring Context OS integrates multiple technologies into one pipeline.

### Main Components

1. Patient Simulator
2. Apache Kafka
3. Context Service
4. Database
5. Neo4j
6. RAG / FAISS
7. LangGraph AI Agent
8. REST API
9. Doctor Dashboard

The system receives patient data, processes it in real time, stores relevant information, retrieves medical knowledge, and generates AI-assisted contextual insights.

---

## 6. System Architecture

```text
                    ┌─────────────────────┐
                    │  Patient Simulator  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Apache Kafka      │
                    │   Message Stream    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Context Service    │
                    │  Kafka Consumer      │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌─────────────┐       ┌─────────────┐
             │  Database   │       │    Neo4j    │
             │ Patient Data│       │ Graph Data  │
             └──────┬──────┘       └──────┬──────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │     RAG + FAISS     │
                    │ Knowledge Retrieval │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  LangGraph AI Agent │
                    │ Patient Reasoning    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      REST API       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Doctor Dashboard   │
                    └─────────────────────┘
```

---

## 7. Technologies Used

| Technology          | Purpose                     |
| ------------------- | --------------------------- |
| Python              | Application development     |
| Apache Kafka 4.2.1  | Real-time data streaming    |
| KRaft               | Kafka cluster management    |
| MySQL / Database    | Patient data storage        |
| Neo4j               | Graph-based patient context |
| FAISS               | Vector similarity search    |
| RAG                 | Medical knowledge retrieval |
| LangGraph           | AI agent workflow           |
| REST API            | Backend communication       |
| Flask               | API and web application     |
| HTML/CSS/JavaScript | Doctor dashboard            |
| Git/GitHub          | Version control             |

---

## 8. Project Structure

```text
patient-monitoring-context-os/
│
├── agent/
│   ├── __init__.py
│   └── agent.py
│
├── api/
│   └── app.py
│
├── architecture/
│
├── context-service/
│   └── kafka_consumer.py
│
├── database/
│
├── frontend/
│   ├── app.py
│   └── templates/
│       └── dashboard.html
│
├── kafka/
│   └── kafka_2.13-4.2.1/
│
├── neo4j/
│
├── patient-simulator/
│   └── simulator.py
│
├── rag/
│   ├── __init__.py
│   ├── ai_context.py
│   ├── build_index.py
│   ├── knowledge_base.txt
│   ├── patient_rag.py
│   └── query.py
│
├── sample/
│
├── .gitignore
├── README.md
└── requirements.txt
```

> The local Kafka installation is ignored from Git using `.gitignore`. Generated RAG files such as `faiss.index` and `metadata.pkl` are also not committed.

---

## 9. Installation

### Clone the repository

```bash
git clone https://github.com/Vaibhav724-web/patient-monitoring-context-os.git
```

```bash
cd patient-monitoring-context-os
```

### Create virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 10. How to Run

The system consists of multiple services. Start the required components according to the project configuration.

### Step 1: Start Kafka

Go to the Kafka directory:

```bash
cd kafka/kafka_2.13-4.2.1
```

Check Kafka version:

```bash
bin/kafka-topics.sh --version
```

Expected:

```text
4.2.1
```

Start Kafka:

```bash
bin/kafka-server-start.sh config/server.properties
```

---

### Step 2: Run Patient Simulator

Open another terminal:

```bash
cd ~/patient-monitoring-context-os
source venv/bin/activate
```

Run:

```bash
python patient-simulator/simulator.py
```

The simulator generates patient information such as:

```json
{
  "patient_id": "P001",
  "timestamp": "2026-09-10T12:32:38.922160",
  "heart_rate": 115,
  "spo2": 91,
  "temperature": 38.5,
  "blood_pressure": "145/90",
  "movement": "low",
  "location": "ICU-12"
}
```

---

### Step 3: Start Context Service

Run:

```bash
python context-service/kafka_consumer.py
```

The context service consumes patient events from Kafka and processes the incoming data.

---

### Step 4: Build RAG Index

Go to the RAG directory:

```bash
cd rag
```

Build the FAISS index:

```bash
python build_index.py
```

This generates the local vector index used for medical knowledge retrieval.

---

### Step 5: Run AI Agent

The LangGraph-based agent is implemented in:

```text
agent/agent.py
```

It processes patient context and retrieved medical information to generate AI-assisted analysis.

---

### Step 6: Start REST API

Run:

```bash
python api/app.py
```

The API provides backend access to patient information and AI-generated results.

---

### Step 7: Start Doctor Dashboard

Run:

```bash
python frontend/app.py
```

The dashboard provides a visual interface for monitoring patients and viewing contextual information.

---

## 11. API Endpoints

The REST API provides endpoints for communication between the backend and frontend.

Typical API functionality includes:

* Patient information
* Current vital signs
* Patient context
* AI analysis
* Patient trends
* Monitoring information

The exact endpoints are implemented in:

```text
api/app.py
```

---

## 12. RAG and FAISS

The project uses **Retrieval-Augmented Generation (RAG)** to provide relevant medical knowledge to the AI system.

### RAG Workflow

```text
Patient Data
     ↓
Patient Context
     ↓
Query Generation
     ↓
FAISS Similarity Search
     ↓
Relevant Medical Knowledge
     ↓
AI Agent
     ↓
Contextual Response
```

The medical knowledge base is stored in:

```text
rag/knowledge_base.txt
```

The RAG implementation includes:

```text
rag/build_index.py
rag/patient_rag.py
rag/query.py
rag/ai_context.py
```

FAISS is used for efficient vector similarity search.

---

## 13. LangGraph AI Agent

The project uses **LangGraph** to implement the AI reasoning workflow.

The agent combines:

* Patient information
* Current vital signs
* Patient context
* Retrieved medical knowledge
* Trend information

The AI agent can then provide contextual analysis rather than relying only on a single vital sign.

The implementation is located in:

```text
agent/agent.py
```

---

## 14. Trend Analysis

Patient vital signs can be analyzed over time to identify changes and abnormal trends.

Examples include:

* Increasing heart rate
* Decreasing SpO2
* Increasing temperature
* Changes in blood pressure
* Reduced movement

Trend analysis helps provide additional context when evaluating the patient's current condition.

---

## 15. Doctor Dashboard

The Doctor Dashboard provides a user-friendly interface for monitoring patient information.

The dashboard can present:

* Patient ID
* Heart rate
* SpO2
* Temperature
* Blood pressure
* Movement
* Location
* Patient status
* Contextual information
* AI-generated insights
* Trend information

Frontend files:

```text
frontend/app.py
frontend/templates/dashboard.html
```

---

## 16. Results

The completed system demonstrates an end-to-end patient monitoring pipeline:

```text
Patient Data
      ↓
Kafka Streaming
      ↓
Context Processing
      ↓
Database / Graph Storage
      ↓
RAG Knowledge Retrieval
      ↓
LangGraph AI Analysis
      ↓
REST API
      ↓
Doctor Dashboard
```

The system successfully integrates real-time patient monitoring with contextual processing and AI-assisted analysis.

---

## 17. Limitations

The current system has some limitations:

1. Patient data is generated using a simulator rather than real medical devices.
2. AI-generated information should not replace professional medical judgment.
3. The medical knowledge base depends on the information provided to the RAG system.
4. Production deployment would require additional security and privacy mechanisms.
5. Real hospital integration would require appropriate healthcare standards and compliance.

---

## 18. Future Scope

Future improvements may include:

* Integration with real IoT medical sensors
* Wearable device integration
* Real hospital monitoring systems
* Advanced predictive analytics
* Early warning prediction
* Improved medical knowledge bases
* Authentication and role-based access
* Secure cloud deployment
* Patient-specific AI models
* Mobile application
* Real-time alert notifications
* Integration with Electronic Health Records
* Advanced graph-based patient reasoning

---

## 19. Team Members

| Member              | Contribution                                                                     |
| ------------------- | -------------------------------------------------------------------------------- |
| **Vaibhav Dhale**   | Patient Monitoring Context OS development, system integration and implementation |
| **Gunjan Mahajan** | Project development, testing and integration                                     |

### Team Contribution

The project was developed collaboratively using Git and GitHub.

The repository follows a version-controlled development workflow so that team members can work on different components and integrate their changes safely.

---

## License

This project is developed for academic and educational purposes.

---

## Repository

**GitHub Repository:**

https://github.com/Vaibhav724-web/patient-monitoring-context-os

