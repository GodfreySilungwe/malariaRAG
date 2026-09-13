# Design and Evaluation

## Design and Architecture Decisions

### Retrieval-augmented generation

The application retrieves relevant chunks from malaria-policy documents before asking the language model to answer. This grounds responses in the supplied corpus and allows the application to return supporting sources rather than relying only on model memory.

### Document processing and storages

PDF files are loaded with LangChain document loaders, split with a recursive character splitter, embedded with `sentence-transformers/all-MiniLM-L6-v2`, and persisted in Chroma. Chroma was selected because it is simple to run locally and integrates with the LangChain retrieval workflow.

### Retrieval and prompting

The default retrieval depth is `TOP_K = 4`, balancing context coverage and prompt size. The prompt instructs the model to use only retrieved context, answer concisely, preserve inline citation markers, and avoid unsupported claims.

### Model integration

The model adapter uses the OpenAI-compatible OpenRouter API. This keeps the application provider-flexible while allowing a remote hosted model to generate answers without serving an LLM locally.

### Application interfaces

Flask provides the `/health`, `/chat`, and frontend-serving routes. React provides the browser UI. The optional Streamlit client remains available for local experimentation but is not required by the deployed Flask/React service.

### Deployment

Railway builds the repository using the Dockerfile and starts `python app.py`. Flask binds to Railway's injected `PORT`. GitHub Actions runs the test suite before deploying pushes to `main` with the Railway CLI.

## Evaluation Approach

The repository uses three layers of evaluation:

1. **Automated regression tests** in `tests/test_malaria_rag.py` cover source formatting, page extraction, response fields, Flask health/chat validation, and refusal configuration.
2. **Evaluation harness** in `evaluate.py` runs questions from `eval_questions.json`, records answers and source metadata, and calculates p50 and p95 latency.
3. **Human review** checks whether each answer is supported by its retrieved policy passages and whether citations identify the correct document and page.

Recommended review criteria are:

- Groundedness: claims are supported by retrieved policy text.
- Citation accuracy: citations identify the relevant document and page.
- Refusal behavior: unsupported questions receive the refusal response.
- Latency: compare p50 and p95 response times.

Run the automated checks with:

```bash
python -m pytest tests/ -v --cov=. --cov-report=xml --tb=short
python evaluate.py
```

The current automated suite contains 16 tests. Evaluation results are written to `eval_results.json`; model-dependent results require `OPENROUTER_API_KEY` and a populated vector store.
