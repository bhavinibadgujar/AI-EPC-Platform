from __future__ import annotations

from pathlib import Path


def extract_pages(path: str | Path) -> list[dict]:
    file_path = Path(path)
    if file_path.suffix.lower() == ".pdf":
        try:
            import fitz

            doc = fitz.open(str(file_path))
            pages = [{"page": index + 1, "text": page.get_text().strip()} for index, page in enumerate(doc)]
            doc.close()
            return [page for page in pages if page["text"]]
        except Exception:
            pass

    text = file_path.read_bytes().decode("utf-8", errors="ignore").strip()
    return [{"page": 1, "text": text}] if text else []
