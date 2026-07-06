"""Ingestion script: load markdown/txt/pdf files, chunk, embed, and persist vector store."""
from pathlib import Path
import argparse
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import context as context_module


def load_text_files(path: Path):
    docs = []
    for p in path.rglob("*.md"):
        text = p.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": p.name}))
    for p in path.rglob("*.txt"):
        text = p.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": p.name}))
    return docs


def run_ingest(data_path: str, persist_path: str = "./chromadb"):
    p = Path(data_path)
    path_docs = load_text_files(p)

    # Also try PDF loader from existing context loader
    try:
        pdf_docs = context_module.load_context_data(path=str(p))
    except Exception:
        pdf_docs = []

    all_docs = path_docs + pdf_docs

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100, length_function=len, is_separator_regex=False
    )
    chunks = splitter.split_documents(all_docs)

    embedding_model = context_module.get_embedding_model()
    vs = context_module.create_vector_store(chunks, embedding_model, path=persist_path)
    print(f"Persisted {len(chunks)} chunks to {persist_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="./corpus", help="Path to corpus files (md/txt/pdf)")
    parser.add_argument("--persist", default="./chromadb", help="Path to persist vector DB")
    args = parser.parse_args()
    run_ingest(args.data, args.persist)
