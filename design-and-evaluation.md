# Design and Evaluation

## Design choices

- The application uses a retrieval-augmented generation pipeline that first ingests policy documents, chunks them, embeds them, and stores them in a local Chroma vector store.
- Embedding model: sentence-transformers/all-MiniLM-L6-v2 via langchain-huggingface was chosen because it provides a good balance of quality and efficiency for local development and keeps the setup lightweight.
- Chunking: documents are split with a recursive character splitter at roughly 800 tokens with 100 tokens of overlap. This keeps each chunk self-contained enough for retrieval while preserving context across boundaries.
- Retrieval depth: the system uses top-k retrieval with k=4. This is a practical compromise between relevance, latency, and prompt size.
- Prompt format: the prompt explicitly tells the model to use only the provided context, answer concisely, include inline citations, and return structured source metadata for the UI.
- Vector store: Chroma was selected because it is easy to run locally, supports persistent storage under the repository, and integrates cleanly with the embedding workflow.
- The backend exposes a Flask API for the browser app and a Streamlit UI for a lightweight local chat demo.

## System architecture

1. Ingestion: policy documents in the corpus folder are parsed and chunked.
2. Indexing: chunks are embedded and persisted in Chroma under the chromadb folder.
3. Retrieval: the backend retrieves relevant chunks for the user question.
4. Generation: the LLM produces an answer with inline citations and the backend returns structured sources, snippets, and latency metadata.
5. Presentation: the Flask/React UI and the Streamlit UI render the main answer, citations, and supporting snippets.

## Evaluation approach

- The repository includes evaluation questions in eval_questions.json.
- The script evaluate.py runs the evaluation set and records answers and latency.
- The current implementation supports automated latency measurement and a human-review workflow for groundedness and citation accuracy.
- Recommended evaluation metrics:
  - Groundedness: confirm that each answer is supported by the retrieved context.
  - Citation accuracy: confirm that each citation points to the correct source or passage.
  - Latency: measure p50 and p95 response times over multiple requests.

## Suggested evaluation workflow

```bash
python evaluate.py
```

Review the generated output in eval_results.json and inspect whether the retrieved sources genuinely support each answer.
