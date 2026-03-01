# 🤖 Semi-Autonomous AI Job Application Agent (LangGraph)

A **semi-autonomous, agentic AI system** that parses resumes, discovers relevant job postings, evaluates suitability using LLM reasoning, and enables **human-in-the-loop job applications**.

Built using **LangGraph**, **Google Gemini**, and **RapidAPI**, this project demonstrates how to design a **stateful multi-agent workflow** rather than a simple automation script.

---

## 🚀 Key Features

- 📄 **Resume Parsing Agent**
  - Extracts structured resume data from PDF files using Google Gemini
  - Automatically caches parsed resumes to avoid repeated LLM calls

- 🔍 **Job Search Agent**
  - Fetches recent internship roles (ML / AI / Analytics) using RapidAPI (JSearch)
  - Supports filters such as role, remote jobs, and posting recency

- 🧠 **LLM-Based Job Evaluation Agent**
  - Uses Gemini reasoning to:
    - Compare multiple resumes against a job description
    - Select the best-fit resume
    - Assign a match score
    - Provide natural-language reasoning

- 👤 **Human-in-the-Loop Review**
  - Presents recommended jobs with reasoning
  - Requires explicit user approval before proceeding

- 📊 **Tracking & Observability**
  - Tracks evaluated jobs, skipped jobs, and failures
  - Clear console metrics during execution

- 🧩 **Agent Orchestration with LangGraph**
  - Stateful execution
  - Conditional routing
  - Safe, deterministic workflow execution

---

## 🧠 Why This Is Agentic (Not Just Automation)

This project goes beyond scripting by introducing:

- Goal-driven decision making  
- LLM-based reasoning instead of hardcoded rules  
- Stateful execution with conditional routing  
- Human approval checkpoints  
- Modular agent design  

Each agent operates with a **clear responsibility**, and LangGraph manages how state flows between them.

---

## 🏗 Architecture Overview
**[ START ]**
    ↓
**Resume Agent** *(or loading from cached )*
    ↓
**Job Search Agent**
    ↓
**Job Evaluation Agent** *(LLM reasoning)*
    ↓
**Human Review Agent**
    ↓
**Tracker Agent**
    ↓
**[ END ]**


---

## ⚙️ Tech Stack

- **Python 3.10+**
- **LangGraph** – Agent orchestration & state management
- **Google Gemini** – Resume parsing & job evaluation
- **RapidAPI (JSearch)** – Job discovery
- **PyPDF2** – Resume text extraction
- **python-dotenv** – Environment variable management

---

## 🔑 Environment Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
RAPIDAPI_KEY=your_rapidapi_key
```
- ⚠️ Gemini API keys must be generated from
- https://aistudio.google.com/app/apikey

---

## 📦 Installation
```
# Create virtual environment
python -m venv venv

# Activate
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install langgraph langchain google-generativeai requests python-dotenv PyPDF2
```
---

## ▶️ How to Run
```
python main.py
```
### Flow:

1. Resumes are parsed (or loaded from cache)

2. Jobs are fetched

3. Each job is evaluated

4. Best match is shown with reasoning

5. User approves or rejects


---

## 🧪 Execution Flow Example
```
⚡ Loaded cached resume for: resume_1.pdf
⚡ Loaded cached resume for: resume_2.pdf

🔎 Total jobs fetched: 12

🤖 Starting Job Evaluation...
🔍 Evaluating: Data Analytics Intern (Remote)
✅ Passed (Score: 0.92)

==============================
REVIEW JOB
==============================
Company: Example Corp
Title: Data Analytics Intern
Score: 0.92
Reason: Strong alignment with analytics projects and SQL skills
Apply Link: https://example.com/apply
==============================
Approve application? (yes/no):
```
--- 

## 📌 Learning Outcomes

This project demonstrates:

- Designing agentic AI systems

- LangGraph state & conditional routing

- LLM reasoning for decision making

- Human-in-the-loop workflows

- Production-oriented debugging & observability