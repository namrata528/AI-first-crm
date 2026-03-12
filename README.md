# AI-first-crm
# AI-First CRM HCP Module – Log Interaction Screen

## Project Overview
This project demonstrates an **AI-First Customer Relationship Management (CRM) system** focused on the **Healthcare Professional (HCP) module**. The purpose of this system is to help pharmaceutical field representatives log and manage their interactions with healthcare professionals such as doctors.

The application allows users to record interactions using two methods:

1. **Structured Form Interface**
2. **AI Conversational Chat Interface**

The system uses an **AI agent built with LangGraph** to interpret user input, extract relevant information, and perform CRM operations using different tools.

---

## Features

### Log Interaction Screen
Users can log interactions with healthcare professionals including:

- Doctor Name  
- Hospital or Clinic  
- Discussion Topic  
- Meeting Summary  
- Follow-up Date  


The AI system extracts important information and stores it in the database.

---

## LangGraph AI Agent Tools

The AI agent manages CRM operations using the following tools:

### 1. Log Interaction Tool
Captures and stores interaction details between a field representative and a healthcare professional.  
The AI extracts entities such as doctor name, hospital name, discussion topic, and follow-up information.

### 2. Edit Interaction Tool
Allows users to modify previously recorded interactions such as updating the follow-up date or correcting meeting details.

### 3. View Interaction History
Displays past meetings or interactions with a specific healthcare professional.

### 4. AI Meeting Summary Tool
Generates a concise AI-based summary of the meeting discussion.

### 5. Follow-up Reminder Tool
Suggests future follow-ups to help sales representatives maintain regular engagement with doctors.

---

## Tech Stack

### Frontend
- React
- Redux
- Google Inter Font

### Backend
- Python
- FastAPI

### AI Framework
- LangGraph

### Language Model
- Groq API
- Gemma2-9b-it model

### Database
- MySQL / PostgreSQL

---

## System Architecture

The application follows a three-layer architecture:

Frontend (React)  
↓  
Backend API (FastAPI)  
↓  
LangGraph AI Agent  
↓  
Database (SQL)

Workflow:

1. The **React frontend** sends requests to the FastAPI backend.
2. The **FastAPI backend** processes the request.
3. The **LangGraph agent** determines which tool should be used.
4. Interaction data is stored or retrieved from the database.


---

## Example Workflow

1. User opens the **Log Interaction Screen**
2. User logs interaction using form or chat
3. AI agent processes the request
4. Appropriate LangGraph tool is triggered
5. Interaction data is saved in database
6. User can view or edit interactions later

---

## Learning Outcomes

This project demonstrates how **AI agents can be integrated into enterprise CRM systems** to automate workflows and improve productivity.

Key learnings include:

- AI-driven workflows using LangGraph
- Integrating LLMs into web applications
- Designing AI-assisted CRM systems
- Full-stack architecture using React and FastAPI

---

## Author

Namrata Shinde  
Assignment Submission – AI-First CRM HCP Module

