from pathlib import Path

from backend.app.rag.ingest import extract_pages


def test_extract_pages_reads_text_file(tmp_path: Path):
    path = tmp_path / "sample.txt"
    path.write_text("Generator load bank test", encoding="utf-8")

    pages = extract_pages(path)

    assert pages == [{"page": 1, "text": "Generator load bank test"}]
