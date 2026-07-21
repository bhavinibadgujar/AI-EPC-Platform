from pathlib import Path

from backend.app.rag.ingest import extract_pages


def test_pdf_ingest_falls_back_to_text(tmp_path: Path):
    path = tmp_path / "note.txt"
    path.write_text("Fire suppression sign-off", encoding="utf-8")

    assert extract_pages(path)[0]["text"] == "Fire suppression sign-off"
