from __future__ import annotations

import math
from collections import Counter


class SimpleVectorStore:
    def __init__(self) -> None:
        self._chunks: list[dict] = []

    @property
    def chunks(self) -> list[dict]:
        return self._chunks

    def index_pages(self, document: str, pages: list[dict], chunk_size: int = 120) -> None:
        for page in pages:
            words = page.get("text", "").split()
            for start in range(0, len(words), chunk_size):
                chunk = " ".join(words[start : start + chunk_size]).strip()
                if chunk:
                    self._chunks.append(
                        {
                            "document": document,
                            "page": page.get("page", 1),
                            "snippet": chunk[:500],
                            "_tokens": Counter(chunk.lower().split()),
                        }
                    )

    def retrieve(self, query: str, k: int = 3) -> list[dict]:
        q = Counter(query.lower().split())
        scored = []
        for chunk in self._chunks:
            score = sum(q[token] * chunk["_tokens"].get(token, 0) for token in q)
            norm = math.sqrt(sum(v * v for v in chunk["_tokens"].values())) or 1
            if score:
                scored.append((score / norm, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [{key: value for key, value in chunk.items() if not key.startswith("_")} for _, chunk in scored[:k]]

    def clear(self) -> None:
        self._chunks.clear()
