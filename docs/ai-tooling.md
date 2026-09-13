# AI Tooling

## Tools Used

- **GitHub Copilot**: assisted with implementation, debugging, test interpretation, deployment configuration, and documentation editing.
- **LangChain**: provided document abstractions, message construction, text splitting, and model orchestration.
- **Hugging Face sentence-transformers**: generated local document embeddings.
- **Chroma**: persisted and queried the document vector store.
- **OpenRouter**: provided the OpenAI-compatible remote language-model endpoint.

## What Worked Well

- Copilot helped trace deployment logs to distinguish build warnings, port detection, memory pressure, and application errors.
- Small test-focused changes made it possible to verify retrieval formatting and API behavior without making live model calls in every test.
- Existing libraries reduced the amount of custom code needed for PDF loading, chunking, embeddings, and vector storage.

## Limitations and Lessons

- AI-generated deployment assumptions required verification against the actual Railway logs and service URLs.
- Documentation can become stale when the deployment provider changes, so the final instructions were checked against the active Railway workflow.
- The test suite uses mocks for model calls; end-to-end answer quality and citation groundedness still require the evaluation harness and human review with a configured API key.

All API keys and deployment tokens are kept outside the repository in `.env`, Railway Variables, or GitHub Actions Secrets.
