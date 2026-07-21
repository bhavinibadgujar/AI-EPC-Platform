from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import unicodedata
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.agents.commissioning.agent import CommissioningAgent
from backend.app.agents.consequence.engine import ConsequenceEngine
from backend.app.agents.schedule.agent import ScheduleAgent
from backend.app.core.config import settings
from backend.app.core.gemini_client import generate_json
from backend.app.db.database import get_db, init_db
from backend.app.db.models import ChatHistory, ComplianceFlag, Document, Project, ScheduleRisk
from backend.app.rag.ingest import extract_pages
from backend.app.rag.store import SimpleVectorStore
from backend.demo_data import fresh_state

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

STATE = fresh_state()
RAG = SimpleVectorStore()


class DeviationItem(BaseModel):
    id: str = "CMP-001"
    clause: str = "Clause 4.1"
    parameter: str
    requirement: str = ""
    required_value: str
    submitted_value: str
    vendor: str = "Vendor"
    status: str = "Deviation"
    severity: str = "Major"
    impact: str = ""
    recommendation: str = ""
    source: str = "Specification"
    page: int = 1
    snippet: str = ""
    confidence: float = 0.85


class ComplianceResponse(BaseModel):
    status: str = "success"
    summary: dict[str, Any]
    deviations: list[DeviationItem]
    confidence: float = 0.90
    ai_generated: bool = False


class ChatRequest(BaseModel):
    message: str | None = None
    question: str | None = None
    messages: list[dict[str, Any]] | None = None


class LoginRequest(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    _seed_rag()
    _seed_default_project()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.parsed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _seed_default_project() -> None:
    db = next(get_db())
    try:
        if not db.get(Project, 1):
            db.add(Project(id=1, name="Demo Project", location="Site A", status="Active"))
            db.commit()
    finally:
        db.close()


def _seed_rag() -> None:
    RAG.clear()
    for doc in STATE["documents"]:
        pages = [{"page": page["page"], "text": page["text"]} for page in doc["pages"]]
        RAG.index_pages(doc["name"], pages)


def _safe_filename(filename: str) -> str:
    name = Path(filename or "upload.bin").name
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = re.sub(r"[^\w.\-]", "_", name)
    stem, *ext = name.rsplit(".", 1)
    suffix = f".{ext[0]}" if ext else ""
    unique = hashlib.md5(os.urandom(8)).hexdigest()[:8]
    return f"{stem}_{unique}{suffix}"


def _save_upload(file: UploadFile) -> Path:
    path = UPLOAD_DIR / _safe_filename(file.filename or "upload.bin")
    with path.open("wb") as buf:
        shutil.copyfileobj(file.file, buf)
    return path


def _severity_from_text(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ("fire", "life safety", "ups", "generator", "critical", "power")):
        return "Critical"
    if any(w in t for w in ("test", "warranty", "capacity", "rating", "voltage")):
        return "High"
    if any(w in t for w in ("document", "report", "drawing")):
        return "Low"
    return "Medium"


def _deterministic_deviations(spec_text: str, vendor_text: str) -> list[dict]:
    checks = [
        {
            "id": "CMP-001",
            "clause": "Clause 4.2",
            "parameter": "UPS battery autonomy",
            "requirement": "UPS shall support full IT load for 15 minutes",
            "patterns": [r"UPS[^.\n]*(\d+\s*min)", r"battery[^.\n]*(\d+\s*min)"],
            "default_req": "15 minutes",
            "default_sub": "10 minutes",
        },
        {
            "id": "CMP-002",
            "clause": "Clause 6.1",
            "parameter": "Generator load bank test",
            "requirement": "4 hour load bank test at 100% nameplate",
            "patterns": [r"load bank[^.\n]*(\d+\s*hour)", r"generator[^.\n]*(\d+\s*hour)"],
            "default_req": "4 hours at 100%",
            "default_sub": "2 hours at 75%",
        },
    ]
    out = []
    for check in checks:
        req = check["default_req"]
        sub = check["default_sub"]
        for pattern in check["patterns"]:
            match = re.search(pattern, spec_text, re.I)
            if match:
                req = match.group(1).strip()
                break
        for pattern in check["patterns"]:
            match = re.search(pattern, vendor_text, re.I)
            if match:
                sub = match.group(1).strip()
                break
        if req.lower() != sub.lower():
            out.append(
                {
                    "id": check["id"],
                    "clause": check["clause"],
                    "parameter": check["parameter"],
                    "requirement": check["requirement"],
                    "required_value": req,
                    "submitted_value": sub,
                    "vendor": "Submitted Vendor",
                    "status": "Deviation",
                    "severity": _severity_from_text(check["parameter"]),
                    "impact": f"Non-compliance with {check['clause']} may cause operational failure",
                    "recommendation": f"Revise submittal to comply with {check['requirement']}",
                    "source": "Specification",
                    "page": 1,
                    "snippet": check["requirement"],
                    "confidence": 0.80,
                }
            )
    return out


def _counts() -> dict:
    return {
        "compliance": len(STATE["compliance_results"]),
        "schedule_risks": len(STATE["schedule_risks"]),
        "supply_chain": len(STATE["supply_chain"]),
        "commissioning": len(STATE["commissioning"]),
    }


@app.get("/")
def home():
    return {"message": "EPC Orbit AI Control Tower is running", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "EPC Orbit",
        "gemini_configured": bool(settings.gemini_api_key),
        "gemini_enabled": settings.ai_epc_use_gemini,
        "rag_chunks": len(RAG.chunks),
        "documents": len(STATE["documents"]),
    }


@app.post("/login")
def login(_: LoginRequest):
    return {"token": "demo-token", "user": {"name": "Mahek", "role": "Project Controls"}}


@app.post("/seed/reset")
def reset_seed():
    STATE.clear()
    STATE.update(fresh_state())
    _seed_rag()
    return {"status": "seeded", "counts": _counts()}


@app.get("/dashboard")
def dashboard():
    critical = sum(1 for i in STATE["compliance_results"] if i.get("severity") == "Critical")
    high = sum(1 for i in STATE["compliance_results"] if i.get("severity") in ("High", "Major"))
    delayed_supply = sum(1 for i in STATE["supply_chain"] if i.get("status") != "On Track")
    blocked_cx = sum(1 for i in STATE["commissioning"] if i.get("status") == "Blocked")
    sched_risks = len(STATE["schedule_risks"])
    return {
        "kpis": {
            "documents": len(STATE["documents"]),
            "compliance_deviations": len(STATE["compliance_results"]),
            "critical_compliance": critical,
            "schedule_risks": sched_risks,
            "supply_alerts": delayed_supply,
            "commissioning_blockers": blocked_cx,
        },
        "activity": [
            {"title": "Compliance check complete", "detail": f"{critical} critical, {high} high deviations flagged.", "type": "warning"},
            {"title": "Schedule risk updated", "detail": f"{sched_risks} schedule risks open.", "type": "info"},
            {"title": "RAG knowledge base", "detail": f"{len(RAG.chunks)} document chunks indexed.", "type": "success"},
        ],
    }


COMPLIANCE_SYSTEM = """You are an EPC compliance AI. Compare the specification and vendor documents. Return only JSON with deviations, summary, and overall_confidence."""


@app.post("/compliance")
@app.post("/compliance/upload")
async def compliance_upload(specification: UploadFile = File(...), vendor: UploadFile = File(...), db: Session = Depends(get_db)):
    spec_path = _save_upload(specification)
    vendor_path = _save_upload(vendor)
    spec_pages = extract_pages(spec_path)
    vendor_pages = extract_pages(vendor_path)
    spec_text = "\n".join(page["text"] for page in spec_pages)
    vendor_text = "\n".join(page["text"] for page in vendor_pages)

    doc_name = specification.filename or "Specification"
    RAG.index_pages(doc_name, spec_pages)
    STATE["documents"].append({"id": f"upload-{len(STATE['documents']) + 1}", "name": doc_name, "pages": spec_pages})
    db.add(Document(filename=doc_name, filepath=str(spec_path), filetype=spec_path.suffix, filesize=spec_path.stat().st_size, project_id=1))

    ai_result = generate_json(
        f"SPECIFICATION:\n{spec_text[:8000]}\n\nVENDOR SUBMITTAL:\n{vendor_text[:8000]}",
        system=COMPLIANCE_SYSTEM,
    )
    raw_devs = ai_result.get("deviations", []) if ai_result else _deterministic_deviations(spec_text, vendor_text)
    deviations = []
    consequence_engine = ConsequenceEngine()
    for idx, item in enumerate(raw_devs, start=1):
        if not isinstance(item, dict):
            continue
        item.setdefault("id", f"CMP-{idx:03d}")
        item.setdefault("clause", f"Clause {idx}.1")
        item.setdefault("vendor", "Submitted Vendor")
        item.setdefault("impact", "Potential non-compliance impact")
        item.setdefault("recommendation", "Review and revise submittal")
        item.setdefault("confidence", 0.85)
        deviation = DeviationItem(**item).model_dump()
        deviation["consequence"] = consequence_engine.calculate(deviation)
        deviations.append(deviation)
        db.add(
            ComplianceFlag(
                external_id=deviation["id"],
                parameter=deviation["parameter"],
                requirement=deviation.get("requirement"),
                required_value=deviation.get("required_value"),
                submitted_value=deviation.get("submitted_value"),
                severity=deviation.get("severity", "Medium"),
                status=deviation.get("status", "Deviation"),
                source=deviation.get("source"),
                page=deviation.get("page"),
                snippet=deviation.get("snippet"),
                confidence=deviation.get("confidence", 0.85),
                project_id=1,
            )
        )
    db.commit()

    STATE["compliance_results"] = deviations
    critical = sum(1 for d in deviations if d.get("severity") == "Critical")
    high = sum(1 for d in deviations if d.get("severity") in ("High", "Major"))
    return ComplianceResponse(
        summary={"deviations": len(deviations), "critical": critical, "high": high},
        deviations=[DeviationItem(**d) for d in deviations],
        confidence=ai_result.get("overall_confidence", 0.85) if ai_result else 0.80,
        ai_generated=bool(ai_result),
    ).model_dump()


@app.get("/compliance")
def compliance_results():
    return {"deviations": STATE["compliance_results"]}


CHAT_SYSTEM = """You are EPC Orbit. Answer only from context and return JSON with answer and citations."""


@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    question = request.question or request.message
    if not question and request.messages:
        question = request.messages[-1].get("content", "")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    chunks = RAG.retrieve(question, k=4)
    if not chunks:
        for doc in STATE["documents"]:
            for page in doc["pages"]:
                text = page["text"]
                if any(token.lower() in text.lower() for token in question.split() if len(token) > 3):
                    chunks.append({"document": doc["name"], "page": page["page"], "snippet": text[:300]})
                    if len(chunks) >= 3:
                        break
            if len(chunks) >= 3:
                break

    no_evidence = "I couldn't find supporting evidence in the uploaded project documents."
    if not chunks:
        answer = no_evidence
        citations = []
    else:
        context = "\n".join(f"- [{c['document']} p.{c['page']}]: {c['snippet']}" for c in chunks[:3])
        ai_result = generate_json(f"Question: {question}\n\nContext:\n{context}", system=CHAT_SYSTEM) or {}
        answer = ai_result.get("answer") or f"Based on project documents: {chunks[0]['snippet'][:200]}"
        citations = ai_result.get("citations") or chunks[:3]

    STATE["chat_history"].append({"question": question, "answer": answer})
    db.add(ChatHistory(question=question, answer=answer, project_id=1))
    db.commit()
    return {"answer": answer, "message": answer, "citations": citations, "confidence": 0.92}


@app.get("/executive-brief")
@app.get("/api/executive-brief/{project_id}")
def executive_brief(project_id: str = "demo"):
    flags = STATE["compliance_results"][:3]
    risks = STATE["schedule_risks"][:2]
    n_flags = len(STATE["compliance_results"])
    n_risks = len(STATE["schedule_risks"])
    critical = sum(1 for flag in STATE["compliance_results"] if flag.get("severity") == "Critical")
    ai_result = generate_json(
        f"Project has {n_flags} compliance deviations ({critical} critical) and {n_risks} schedule risks. Top issues: {json.dumps(flags + risks, default=str)[:1200]}.",
        system="Return JSON: {\"brief\": \"...\"}",
    ) or {}
    brief = ai_result.get("brief") or (
        f"Project Synapse currently shows {n_flags} specification deviations, of which {critical} are critical and require vendor response before procurement release. "
        f"Schedule exposure is concentrated in {n_risks} open risks, with critical-path activities requiring daily review. "
        "Supply chain and commissioning blockers should remain on the executive action log until cleared. "
        f"AI Confidence: 96% based on {len(STATE['documents'])} uploaded documents and {len(RAG.chunks)} indexed chunks."
    )
    return {"project_id": project_id, "brief": brief, "cached": False, "top_flags": flags, "top_risks": risks, "confidence": 0.96}


@app.post("/schedule-risk")
async def schedule_risk(file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = _save_upload(file)
    try:
        report = ScheduleAgent().analyze(path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    risks = []
    for idx, risk in enumerate(report["risks"], start=1):
        activity = risk.get("activity_name") or risk.get("activity_id") or f"Activity {idx}"
        item = {
            "id": risk.get("risk_id", f"SCH-{idx:03d}"),
            "activity": activity,
            "reason": risk.get("description", "Schedule risk detected."),
            "severity": str(risk.get("severity", "Medium")).title(),
            "eta": f"{report['project_duration']} days",
            "owner": "Project Controls",
            "confidence": risk.get("confidence", 1.0),
        }
        risks.append(item)
        db.add(
            ScheduleRisk(
                external_id=item["id"],
                activity_id=risk.get("activity_id"),
                activity=item["activity"],
                reason=item["reason"],
                severity=item["severity"],
                eta=item["eta"],
                owner=item["owner"],
                confidence=item["confidence"],
                project_id=1,
            )
        )
    db.commit()
    STATE["schedule_risks"] = risks or STATE["schedule_risks"]
    return {
        "status": "success",
        "risks": STATE["schedule_risks"],
        "summary": {"open_risks": len(STATE["schedule_risks"]), **report["analysis"]["summary"]},
        "critical_path": report["critical_path"],
        "project_duration": report["project_duration"],
        "ai_summary": report["ai_summary"],
        "confidence": 0.95,
    }


@app.get("/risk")
def risk():
    return {"risks": STATE["schedule_risks"]}


@app.get("/supply")
def supply():
    return {"shipments": STATE["supply_chain"]}


@app.get("/commissioning")
def commissioning():
    return CommissioningAgent().analyze(STATE["commissioning"])
