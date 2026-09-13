# MalariaAI RAG

MalariaAI RAG is a retrieval-augmented generation application that answers questions from a local malaria-policy corpus. It provides a Flask API and a React web interface, with an optional Streamlit client for local experimentation.

## Repository

GitHub: https://github.com/GodfreySilungwe/malariaRAG

Live application: https://malariarag-production.up.railway.app/


## Features

- PDF policy ingestion and persistent Chroma storage
- Top-k retrieval with source metadata, snippets, and page numbers
- Context-constrained LLM responses through OpenRouter
- Flask `/health` and `/chat` endpoints
- React chat interface served by Flask
- Automated tests and GitHub Actions deployment to Railway

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- An OpenRouter API key

## Local Setup

```bash
git clone https://github.com/GodfreySilungwe/malariaRAG.git
cd malariaRAG
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies and configure the environment:

```bash
python -m pip install -r requirements.txt
copy .env.example .env
```

Set `OPENROUTER_API_KEY` in `.env`. Never commit `.env` or API keys.

## Run the Application

Build the React interface and start Flask:

```bash
cd frontend
npm install
npm run build
cd ..
python app.py
```

Open `http://localhost:5000`. The API health check is available at `http://localhost:5000/health`.

For separate frontend development, run Flask in one terminal and then:

```bash
cd frontend
npm start
```

The development UI runs at `http://localhost:3000` and proxies API requests to Flask on port 5000.

The optional Streamlit client is not installed by the default Railway/API dependency set. To use it locally, install Streamlit separately:

```bash
python -m pip install streamlit
streamlit run malaria_client.py
```

## API

Health check:

```bash
curl http://localhost:5000/health
```

Chat request:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What are the preventive measures for malaria?"}'
```

The chat response includes `answer`, `snippets`, `sources`, and `latency_ms`.

## Tests and Evaluation

Run the automated tests:

```bash
python -m pytest tests/ -v --cov=. --cov-report=xml --tb=short
```

Run the evaluation harness against `eval_questions.json`:

```bash
python evaluate.py
```

Supporting reports and project documentation are organized in the [`docs/`](docs/) folder:

- [design-and-evaluation.md](docs/design-and-evaluation.md): design decisions, system architecture, and evaluation methodology.
- [evaluation-report.md](docs/evaluation-report.md): question-level groundedness, citation accuracy, latency, and findings.
- [ai-tooling.md](docs/ai-tooling.md): AI tools used, what worked, and limitations.

## Deployment

The active deployment target is Railway. GitHub Actions runs tests on pushes and pull requests. A push to `main` deploys to Railway only after the test job passes.

Required GitHub Actions secrets:

```text
RAILWAY_TOKEN
RAILWAY_PROJECT_ID
RAILWAY_ENVIRONMENT_ID
RAILWAY_SERVICE_ID
```

Required Railway service variable:

```text
OPENROUTER_API_KEY
```

Railway supplies `PORT` automatically. See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for the deployment procedure and [deployed.md](docs/deployed.md) for the public link.

## Project Structure

- `app.py`: Flask server and API routes
- `malaria_rag.py`: retrieval, prompting, and response formatting
- `context.py`: corpus loading, embeddings, and Chroma helpers
- `ingest.py`: corpus ingestion script
- `model.py`: OpenRouter model adapter
- `frontend/`: React web interface
- `tests/`: automated regression and API tests
- `docs/`: supporting documentation and evaluation reports

## Security

Keep API keys in local `.env` files or Railway Variables. Rotate any key that has been exposed and never commit secrets to GitHub.
