# EPC Orbit — AI Intelligence Platform for Data Centre EPC Projects

> A RAG-powered AI platform that helps EPC engineers verify compliance, retrieve project knowledge, and summarise project status directly from uploaded engineering documents — without hallucinating answers from general training data.

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)
![React](https://img.shields.io/badge/React-Vite-61DAFB.svg)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange.svg)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-blueviolet.svg)

---

## The Problem

A typical data centre EPC project generates 200–500 engineering documents — specifications, datasheets, RFIs, inspection reports — across civil, mechanical, and electrical disciplines. Engineers manually cross-reference these documents to check compliance and answer project queries. This is slow, inconsistent, and a bottleneck when project timelines are under pressure.

Generic keyword search doesn't work: a specification might say "maximum allowable temperature" in one document and "thermal limit" in another. General-purpose LLMs can't be trusted: they hallucinate domain-specific answers they weren't trained on.

EPC Orbit solves this by grounding every AI answer in the actual uploaded project documents using Retrieval-Augmented Generation (RAG).

---

## What's Built (Prototype — ET Hackathon 2.0)

| Module | Status | Description |
|---|---|---|
| PDF Upload | ✅ Working | Upload engineering specs and documents for AI processing |
| AI Compliance Agent | ✅ Working | Flags non-conformances at clause level against uploaded specs |
| RAG Knowledge Copilot | ✅ Working | Answers free-form questions grounded in uploaded documents |
| Executive AI Summary | ✅ Working | Generates structured project status brief from document findings |
| Dashboard | ✅ Working | Compliance status, risk overview, uploaded documents |
| Schedule Risk Analysis | 🔧 Scaffolded | Backend structure exists; end-to-end validation incomplete |
| Supply Chain Intelligence | 🔧 Scaffolded | Frontend route exists; agent logic not fully wired |
| Commissioning Copilot | 🔧 Scaffolded | Planned for post-hackathon development |

> **Honesty note:** Scaffolded modules have frontend routes and partial backend structure but were not fully validated within the hackathon window. They are not claimed as working features.

---

## Architecture

```
User (Browser)
      │
      ▼
React + Vite Frontend          ← MUI components, Recharts dashboard, Framer Motion
      │
      ▼  REST (JSON)
FastAPI Backend (Python)        ← Async, auto OpenAPI docs at /docs
      │
      ▼
AI Agent Layer
 ├── Compliance Agent           ← POST /compliance
 │     └── PyMuPDF → Chunker → ChromaDB embed → Gemini → Clause-level findings
 ├── RAG Knowledge Copilot      ← POST /knowledge
 │     └── Query → ChromaDB retrieval → Gemini (context-grounded) → Answer
 ├── Executive Brief Agent      ← POST /executive-summary
 │     └── Aggregates findings → Structured summary via Gemini
 ├── Schedule Risk Agent        ← POST /schedule-risk  [scaffolded]
 └── Commissioning Copilot      ← [planned]
      │
      ▼
ChromaDB (local vector store)   ← Embedded, no cloud dependency
Google Gemini API               ← LLM + embeddings
PyMuPDF                         ← PDF text extraction
```

### Key Architecture Decisions

**RAG over fine-tuning** — Fine-tuning requires labelled domain data we don't have, and bakes knowledge into weights. RAG grounds answers in uploaded documents at inference time — the system works on any EPC project without retraining.

**ChromaDB (embedded)** — Runs in-process with FastAPI, no cloud dependency, no extra infrastructure. Trade-off: not suitable for millions of vectors, but a single EPC project's document set stays well under 50,000 chunks.

**Chunk size: ~500 tokens, 50-token overlap** — Smaller chunks lost cross-sentence compliance clause context. Larger chunks degraded embedding precision. The overlap ensures clause boundaries spanning two chunks remain retrievable.

**PyMuPDF over pdfplumber** — Handles multi-column engineering layouts and large document sizes faster and more accurately for this document class.

**Modular agents, not one monolithic prompt** — Each agent has its own endpoint and responsibility. Failure in one agent does not affect others; each can be tested and improved independently.

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | React + Vite | Fast builds, component isolation |
| UI Components | MUI (Material UI) | Consistent design system without a custom DSL |
| Charts | Recharts | Lightweight, React-native charting |
| Backend | FastAPI | Async, auto docs, clean router structure |
| LLM | Google Gemini | Available via free-tier API, multimodal capable |
| Embeddings | Gemini Embeddings | Same API, avoids a second dependency |
| Vector Store | ChromaDB | Local, embedded, Python-native |
| PDF Parsing | PyMuPDF | Layout-aware, fast on large engineering PDFs |
| Data Processing | Pandas | Schedule data handling |
| Graph Analysis | NetworkX | Critical path computation (schedule agent) |
| Testing | Pytest | Backend unit tests |

---

## Project Structure

```
AI-EPC-Platform/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── agents/
│   │   ├── compliance_agent.py  # Compliance checking logic
│   │   ├── knowledge_agent.py   # RAG copilot logic
│   │   └── executive_agent.py   # Summary generation
│   ├── api/
│   │   └── routes/              # Endpoint definitions
│   └── tests/                   # Pytest test suite
├── epc-ai-copilot/              # React + Vite frontend
│   └── src/
│       └── pages/               # /compliance /chat /risk /dashboard
├── architecture/                # Architecture diagrams
├── dataset/                     # Sample engineering documents
├── demo/                        # Demo assets
├── docs/                        # Documentation
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- Google Gemini API key (free tier at [aistudio.google.com](https://aistudio.google.com))

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/bhavinibadgujar/AI-EPC-Platform.git
cd AI-EPC-Platform

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Start the backend
python -m uvicorn backend.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### Frontend Setup

```bash
cd epc-ai-copilot
npm install
npm run dev
```

Frontend available at: `http://localhost:5173`

### Run Tests

```bash
python -m pytest backend/tests
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/upload` | Upload a PDF for processing |
| POST | `/compliance` | Run compliance check against uploaded specs |
| POST | `/knowledge` | Ask a free-form question from document context |
| POST | `/executive-summary` | Generate a structured project summary |
| POST | `/schedule-risk` | Schedule risk analysis (scaffolded) |
| GET  | `/docs` | Auto-generated OpenAPI documentation |

### Example: Knowledge Copilot Query

```bash
curl -X POST http://127.0.0.1:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the required UPS capacity?", "document_id": "spec-001"}'
```

```json
{
  "answer": "The specification on page 14 requires a minimum UPS capacity of 500 kVA with N+1 redundancy.",
  "source_chunks": ["spec-001_chunk_42", "spec-001_chunk_43"],
  "confidence": "high"
}
```

---

## Roadmap

Post-hackathon development priorities, in order:

1. **Complete Schedule Risk Agent** — NetworkX critical path + Gemini-interpreted delay risk
2. **Complete Commissioning Copilot** — QA checklist validation from commissioning docs
3. **Supply Chain Intelligence** — Vendor lead time risk flagging
4. **RBAC Authentication** — Role-based access for project managers vs. engineers
5. **Cloud Deployment** — Docker + cloud hosting for multi-project use
6. **Computer Vision Drawing Review** — Extend to engineering drawings (not just text PDFs)
7. **ERP / QMS Integration** — Connect to SAP PM, Oracle Primavera

---

## Team

| Name | Role |
|---|---|
| Bhavini Badgujar | AI Agents & Intelligence Layer |
| Brinda Naik | Backend Engineering |
| Mahek Batavia | UI/UX & Frontend |

Built for **ET Hackathon 2.0**

---

## License

MIT License — see [LICENSE](LICENSE) for details.
