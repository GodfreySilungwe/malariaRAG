# 🦟 MalariaAI RAG

MalariaAI RAG is a retrieval-augmented generation application for answering questions about malaria policies using a local corpus of policy documents. The project includes:

- a Flask API with the required endpoints for chat, health, and web access
- a React web UI for the browser-based chat experience
- a Streamlit UI for a simple local chat experience
- a retrieval pipeline backed by Chroma and sentence-transformers embeddings

## Project requirements covered

- Retrieval-augmented generation over a local policy corpus
- Top-k retrieval with citations and snippets
- Inline citations inside the answer text plus a structured citations section
- API and web endpoints for chat and health checks
- Local setup instructions and automated tests

## Local setup

### 1. Prerequisites

- Python 3.10+
- Node.js 18+
- pip and npm
- Git
- An LLM API key such as OpenRouter or another compatible provider

### 2. Clone the repository

```bash
git clone https://github.com/GodfreySilungwe/malariaRAG.git
cd malariaRAG
```

### 3. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy the example file and fill in the required values:

```bash
copy .env.example .env
```

Then update the values in .env, especially:

- OPENROUTER_API_KEY or another model API key
- PORT if you want a different Flask port
- REACT_APP_API_URL if you are running the frontend separately

## Run locally using Streamlit (recommended for quick demo)

This is the simplest way to run the app locally.

### Step-by-step

1. Make sure the virtual environment is active and the dependencies are installed.
2. Create the vector store from the policy corpus if it does not already exist:

```bash
python ingest.py
```

3. Start the Streamlit app:

```bash
streamlit run malaria_client.py
```

4. Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

5. Enter a question in the chat box. The answer will appear with inline citations and a separate citations section below the message.

## Run the Flask API and React UI

### Option A: Run the Flask API only

```bash
python app.py
```

Then open:

- http://localhost:5000/health for the health check
- http://localhost:5000/chat for the API endpoint
- http://localhost:5000 for the React web interface

### Option B: Run the React frontend separately during development

```bash
cd frontend
npm install
npm start
```

The React development server will run at http://localhost:3000 and proxy requests to the Flask backend.

If you want the React build to be served by Flask, build it first:

```bash
cd frontend
npm install
npm run build
cd ..
python app.py
```

## API endpoints

- GET /health returns JSON with the server status.
- POST /chat accepts a JSON body with a question field and returns an answer, snippets, sources, and latency_ms.
- GET / serves the React web chat app.

Example:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What are the preventive measures for malaria?"}'
```

## Testing

Run the test suite with:

```bash
python -m pytest -q
```

## Project structure

- app.py: Flask server and API routes
- malaria_rag.py: retrieval, prompt construction, answer formatting, and source metadata
- malaria_client.py: Streamlit chat UI
- ingest.py: corpus ingestion and vector store creation
- context.py: embedding model and Chroma vector store helpers
- frontend/: React frontend source and build files
- tests/: regression and integration tests

## Documentation

- [design-and-evaluation.md](design-and-evaluation.md)
- [ai-tooling.md](ai-tooling.md)
- [DEPLOYMENT.md](DEPLOYMENT.md)

## Troubleshooting

- If the model cannot answer, verify that OPENROUTER_API_KEY is set correctly.
- If you get a vector store error, rerun python ingest.py.
- If the React UI shows a connection problem, confirm that python app.py is running and that REACT_APP_API_URL points to the correct backend URL.
- If Streamlit cannot find the app, run the command from the repository root.



If ChromaDB fails to initialize:
```bash
# Clear existing database
rm -rf chromadb/

# Re-ingest the corpus
python ingest.py --data ./corpus --persist ./chromadb
```

### API Connection Errors

Ensure the Flask API is running:
```bash
python app.py
# Should print: Running on http://0.0.0.0:8000
```

### Streamlit Connection Issues

Verify the API URL in Streamlit settings:
1. Open the app
2. Click ⚙️ Settings in sidebar
3. Update API URL if needed (default: http://localhost:8000)

### Test Failures

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version: `python --version` (should be 3.10+)
3. View detailed error logs: `pytest tests/ -v -s`

## 📊 Performance Tips

- Use free tier for development, upgrade for production
- Enable response caching for frequently asked questions
- Index policy documents for faster retrieval
- Monitor ChromaDB size and consider archiving old data

## 🔒 Security

- Never commit `.env` files or secrets
- Use GitHub Secrets for API keys
- Run health checks regularly
- Monitor logs for suspicious activity
- Keep dependencies up to date

## 📝 License

[Add your license here]

## 👥 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new features
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check existing [GitHub Issues](https://github.com/yourusername/malariaRAG/issues)
2. Create a new issue with details
3. Include error messages and logs

## 🎯 Roadmap

- [x] Flask API with RAG
- [x] Streamlit Web UI
- [x] JavaScript Web UI (modern, lightweight)
- [x] Docker & Docker Compose support
- [x] GitHub Actions CI/CD pipeline
- [x] Render deployment configuration
- [ ] Database persistence for conversation history
- [ ] User authentication & accounts
- [ ] Rate limiting & usage tracking
- [ ] Advanced search filters
- [ ] Export chat as PDF
- [ ] Conversation sharing
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Analytics dashboard
- [ ] Voice input/output
- [ ] Integration with other data sources

---

**Last Updated:** 2024
**Status:** Production Ready ✅
