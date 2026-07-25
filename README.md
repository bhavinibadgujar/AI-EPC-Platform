# 🚀 EPC Orbit
### AI Intelligence Platform for Data Centre EPC Project Delivery

> An AI-powered platform that transforms Engineering, Procurement, and Construction (EPC) project management using Generative AI, intelligent document analysis, schedule risk prediction, and compliance automation.

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange.svg)

---

## 📖 Overview

Data centre EPC projects involve thousands of documents, vendors, schedules, and quality inspections. Most project information exists across disconnected systems, making compliance verification and project monitoring slow and error-prone.

**EPC Orbit** provides an AI-powered intelligence layer that centralizes project information and enables engineers to:

- Verify compliance automatically
- Analyze project schedules
- Search project documents using AI
- Generate project reports
- Monitor project health from a single dashboard

---

# ✨ Features

## 📄 Smart Document Upload
Upload project specifications, contracts, schedules, and technical documents.

---

## ✅ AI Compliance Checking
Automatically compares uploaded specifications and identifies:

- Missing requirements
- Compliance gaps
- Specification mismatches
- Non-conformance issues

---

## 📅 Schedule Risk Analysis

Uses graph-based dependency analysis to detect:

- Critical paths
- Delay risks
- Task dependency issues
- Schedule bottlenecks

---

## 🤖 AI Knowledge Copilot

Powered by **Google Gemini**

Ask questions like:

> "What is the required UPS capacity?"

> "Which specification mentions cable routing?"

> "Show all HVAC requirements."

---

## 📊 Executive Dashboard

Centralized dashboard showing

- Compliance Status
- Risk Analysis
- Uploaded Documents
- Reports
- Project Overview

---

## 📑 Report Generation

Generate downloadable reports containing

- Compliance Summary
- Schedule Analysis
- AI Findings
- Project Insights

---

# 🏗️ Architecture

```
User
   │
React Frontend
   │
FastAPI Backend
   │
AI Agent Layer
 ├── Compliance Agent
 ├── Knowledge Copilot
 ├── Schedule Risk Agent
 ├── AI Risk Engine
 └── Executive Brief Agent
   │
Gemini API + ChromaDB
   │
Project Documents
```

---

# 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Backend | FastAPI |
| AI Model | Google Gemini |
| Vector Database | ChromaDB |
| Document Processing | PyMuPDF |
| Data Processing | Pandas |
| Graph Analysis | NetworkX |
| Configuration | python-dotenv |
| Testing | Pytest |
| Frontend | JavaScript, CSS |

---

# 📂 Project Structure

```
AI-EPC-Platform/
│
├── backend/
│   ├── app/
│   ├── agents/
│   ├── api/
│   ├── tests/
│
├── architecture/
│
├── dataset/
│
├── demo/
│
├── docs/
│
├── presentation/
│
├── scripts/
│
├── uploads/
│
├── output/
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.9+
- Git
- Google Gemini API Key

---

## Installation

Clone the repository

```bash
git clone https://github.com/bhavinibadgujar/AI-EPC-Platform.git
```

Move into the project

```bash
cd AI-EPC-Platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the backend

```bash
python -m uvicorn backend.app.main:app --reload
```

API Documentation

```
http://127.0.0.1:8000/docs
```

---

# 🧪 Run Tests

```bash
python -m pytest backend
```

---

# 🎯 Current Modules

- ✅ Document Upload
- ✅ AI Compliance Agent
- ✅ Schedule Risk Analysis
- ✅ AI Knowledge Copilot
- ✅ Dashboard
- ✅ Report Generation

---

# 🚧 Future Roadmap

- Commissioning QA Copilot
- Supply Chain Visibility Agent
- Computer Vision Drawing Review
- RBAC Authentication
- Cloud Deployment
- ERP & QMS Integration

---

# 👥 Team

| Name | Role |
|------|------|
| **Bhavini Badgujar** | AI Agents |
| **Brinda Naik** | Backend Engineering |
| **Mahek Batavia** | UI/UX Design |

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 🌟 Why EPC Orbit?

Traditional EPC projects rely on fragmented documents and manual verification.

EPC Orbit introduces an intelligent AI layer that understands project documents, predicts risks, automates compliance, and assists engineers throughout the project lifecycle, improving productivity, reducing delays, and enabling better decision-making.

---

⭐ If you like this project, consider giving it a star!
