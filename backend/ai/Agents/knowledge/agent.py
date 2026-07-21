from app.ai.gemini import generate_json
from app.ai.chroma.store import query
from app.ai.prompts.knowledge_prompts import RAG_ANSWER_PROMPT

class KnowledgeAgent:
    def ask(self, question: str, project_id: str, top_k: int = 5) -> dict:
        results = query("project_docs", question, top_k=top_k)

        documents = results.get("documents", [[]])[0]
        ids = results.get("ids", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if not documents:
            return {"answer": "I don't have information on that in the project documents.", "cited_chunk_ids": []}

        context_blocks = []
        for chunk_id, doc, meta in zip(ids, documents, metadatas):
            context_blocks.append(f"[{chunk_id}] (source: {meta.get('source', 'unknown')})\n{doc}")
        context = "\n\n".join(context_blocks)

        prompt = RAG_ANSWER_PROMPT.format(context=context, question=question)
        return generate_json(prompt)

    def index_document(self, doc_id: str, text: str, source_name: str, chunk_size: int = 300):
        from app.ai.chroma.store import add_chunk
        words = text.split()
        chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_chunk_{idx}"
            add_chunk("project_docs", chunk_id, chunk, {"source": source_name, "doc_id": doc_id})