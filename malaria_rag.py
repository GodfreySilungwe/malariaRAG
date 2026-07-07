"""RAG utilities for PraxaApp (renamed for malaria corpus).

Provides retrieval, prompting with guardrails, citation extraction,
and a simple answer API used by the Flask backend.
"""
from typing import List, Tuple
import re
import time

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage

import context as context_module
import model as model_module


# Configuration
TOP_K = 4
REFUSE_TEMPLATE = (
    "I can only answer questions using the provided policy documents. "
    "If the answer is not supported by those documents, I will say so."
)


def _extract_page_number(doc: Document):
    """Extract a page number from document metadata when present."""
    for key in ("page", "page_number", "page_num"):
        value = doc.metadata.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            return value
    return None


def get_source_label(doc: Document, index: int) -> str:
    """Build a display label for a source, including page numbers when available."""
    title = doc.metadata.get("source") or doc.metadata.get("title") or f"doc_{index}"
    page_number = _extract_page_number(doc)
    if page_number is None:
        return title
    return f"{title} (page {page_number})"


def retrieve_docs_with_scores(query: str, k: int = TOP_K) -> List[Tuple[Document, float]]:
    """Retrieve top-k documents with similarity scores from the vector store.

    Falls back to returning documents without scores if the store does not
    provide scores.
    """
    vs = context_module.get_vector_store()
    try:
        results = vs.similarity_search_with_score(query, k=k)
        return results
    except Exception:
        # fallback: similarity_search returns just documents
        docs = vs.similarity_search(query, k=k)
        return [(d, None) for d in docs]


def build_context_text(docs: List[Document]) -> str:
    """Create a combined context string with inline numbered sources."""
    parts = []
    for i, doc in enumerate(docs, start=1):
        title = get_source_label(doc, i)
        snippet = doc.page_content[:800].strip()
        parts.append(f"[{i}] {title}\n{snippet}")
    return "\n\n".join(parts)


def format_sources(docs: List[Document]) -> List[dict]:
    """Return structured source entries for JSON responses."""
    out = []
    for i, doc in enumerate(docs, start=1):
        page_number = _extract_page_number(doc)
        title = doc.metadata.get("source") or doc.metadata.get("title") or f"Document {i}"
        citation = title if page_number is None else f"{title} (page {page_number})"
        out.append({
            "id": i,
            "source": get_source_label(doc, i),
            "document": title,
            "page": page_number,
            "page_number": page_number,
            "citation": citation,
            "meta": doc.metadata,
        })
    return out


def clean_answer_text(text: str) -> str:
    """Normalize the answer text while preserving inline citation markers."""
    if not text:
        return text

    cleaned = re.sub(r"(?im)^\s*(citations?|references?)\s*:.*$", "", text)
    cleaned = re.sub(r"\n\s*\n\s*(citations?|references?)\s*:.*", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def answer_and_sources(question: str, top_k: int = TOP_K, max_tokens: int = 512) -> dict:
    """Answer a question using retrieval augmented generation.

    Returns JSON-friendly dict with `answer`, `sources`, `snippets`, and `latency_ms`.
    """
    start = time.time()
    results = retrieve_docs_with_scores(question, k=top_k)
    docs = [r[0] for r in results]

    if not docs:
        return {"answer": REFUSE_TEMPLATE, "sources": [], "snippets": [], "latency_ms": int((time.time()-start)*1000)}

    context_text = build_context_text(docs)

    system = SystemMessage(content=(
        "You are an assistant that answers questions using ONLY the provided context. "
        "If the answer cannot be found in the context, reply: 'I don't know based on the provided policies.' "
        "Write a concise answer paragraph and include inline citations in the form [n] where relevant. "
        "Also provide a separate citations section through the structured source metadata."))

    human = HumanMessage(content=(
        f"Context:\n{context_text}\n\nQuestion: {question}\n\n"
        "Provide a short answer paragraph with inline citations like [1] where the answer is supported by the context. "
        "Do not add a separate citations list in the answer text."))

    chat_model = model_module.get_model()
    try:
        response = chat_model.invoke([system, human])
        text = clean_answer_text(response.content)
    except Exception as e:
        text = f"Error invoking model: {e}"

    latency = int((time.time() - start) * 1000)

    return {
        "answer": text,
        "snippets": [d.page_content[:500] for d in docs],
        "sources": format_sources(docs),
        "latency_ms": latency,
    }


if __name__ == "__main__":
    # basic local demo
    q = "What is the recommended treatment for uncomplicated malaria in adults?"
    out = answer_and_sources(q)
    print(out)
