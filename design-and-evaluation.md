# Design and Evaluation

Short notes on design choices and evaluation approach.

- Embedding model: `sentence-transformers/all-MiniLM-L6-v2` via `langchain-huggingface` for good quality with low compute.
- Vector store: `Chroma` persisted locally under `./chromadb`.
- Chunking: `RecursiveCharacterTextSplitter` with `chunk_size=800`, `chunk_overlap=100`.
- Retrieval: top-k similarity search (k=4) with optional score-based re-ranking if supported.
- Prompting: explicit system instruction to only use provided context, include citations, and limit length.

Evaluation:

- `eval_questions.json` contains 15 policy questions.
- `evaluate.py` runs the questions, records answers and latency, and writes `eval_results.json`.
- Metrics: groundedness and citation accuracy require human judgment (not automated here); latency (p50/p95) is computed automatically.
