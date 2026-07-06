# PraxaApp — RAG backend for Malaria Policies

This workspace contains a Retrieval-Augmented Generation backend used to answer questions about malaria policies.

Quick start:

1. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Ingest the sample corpus (or add your own files to `corpus/`):

```bash
python ingest.py --data ./corpus --persist ./chromadb
```

3. Run the Flask backend:

```bash
python app.py
```

4. Use the React frontend (not included) or `curl` to call `/chat`:

```bash
curl -X POST localhost:8000/chat -H "Content-Type: application/json" -d '{"question":"What is the recommended treatment for uncomplicated malaria?"}'
```
