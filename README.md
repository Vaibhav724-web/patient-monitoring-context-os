# patient-monitoring-context-os
AI-based real-time patient monitoring and context management system
# Patient Monitoring Context OS

## Project Overview

Patient Monitoring Context OS is an intelligent patient monitoring
system that continuously monitors patient vital signs such as
Heart Rate, SpO2, Temperature and Blood Pressure.

The system detects abnormal changes, maintains current and historical
patient context, retrieves relevant medical monitoring knowledge,
and generates grounded alerts/recommendations for healthcare staff.

## Problem Statement

Patient vital signs can change rapidly, especially in critical care
environments. Therefore, continuous monitoring is required to
identify abnormal changes and provide timely information to doctors
and nurses.

## System Architecture

Patient Simulator
        |
        v
      Kafka
        |
        v
 Context Engine
        |
        v
Redis / PostgreSQL / Neo4j
        |
        v
    RAG / FAISS
        |
        v
 LangGraph Agent
        |
        v
    REST API
        |
        v
Doctor / Nurse Dashboard

## Technologies

- Python
- Apache Kafka
- Redis
- PostgreSQL
- Neo4j
- FAISS
- RAG
- LangGraph
- REST API
- Frontend

## Team Members

1. Gunjan Mahajan
2. Vaibhav Dhale

## Project Guide

Sumit Badase Sir
