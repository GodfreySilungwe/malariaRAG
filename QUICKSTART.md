# 🚀 Quick Start Guide

Get MalariaAI RAG up and running in 5 minutes!

## Prerequisites

- Python 3.10+ & pip
- Node.js 18+ & npm
- OpenAI API Key
- Git

## ⚡ 5-Minute Setup

### Step 1: Clone & Install (2 min)

```bash
# Clone
git clone https://github.com/GodfreySilungwe/malariaRAG.git
cd malariaRAG

# Create Python environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
# OR
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### Step 2: Configure (1 min)

```bash
cp .env.example .env
# Edit .env file and add your OPENAI_API_KEY
```

### Step 3: Build React (1 min)

```bash
cd frontend && npm run build && cd ..
```

### Step 4: Run (1 min)

```bash
python app.py
# Open http://localhost:5000 in your browser
```

---

## 🐳 Or Use Docker (Even Faster!)

```bash
docker-compose up --build
# Open http://localhost:5000
```

---

## 🧪 Test It

```bash
# Run tests
pytest tests/ -v

# Or use the test script
./run_tests.sh      # macOS/Linux
run_tests.bat       # Windows
```

---

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:5000/health
# Response: {"status": "ok"}
```

### Ask a Question
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What are malaria preventive measures?"}'
```

**Response:**
```json
{
  "answer": "According to the policies...",
  "sources": [{"document": "malaria_policy_1.md", "page": 3}]
}
```

---

## 🚀 Deploy to Render

1. **Ensure git is ready:**
   ```bash
   git add .
   git commit -m "Initial Flask + React setup"
   git push origin main
   ```

2. **GitHub Actions will automatically:**
   - Run tests
   - Build React
   - Deploy to Render

3. **Visit your deployed app:**
   - `https://malaria-rag-api.onrender.com`

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Frontend not loading | `cd frontend && npm run build && cd ..` |
| Port 5000 in use | Change `PORT` in `.env` |
| API connection failed | Check health: `curl http://localhost:5000/health` |
| Module not found | Run `pip install -r requirements.txt` |

---

## 📁 Key Files

- `app.py` - Flask API server
- `frontend/` - React application
- `malaria_rag.py` - RAG system logic
- `.env.example` - Environment template
- `docker-compose.yml` - Docker setup

---

## 🧠 Frontend Development

To develop React with hot-reload:

```bash
cd frontend
npm start
# Opens http://localhost:3000
# Proxies API to http://localhost:5000
```

---

## 📖 More Documentation

- [README.md](README.md) - Full guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [ai-tooling.md](ai-tooling.md) - AI configuration

---

**Next**: Read [README.md](README.md) for comprehensive documentation!

✅ **Ready to go!**
- [ ] API running locally (`python app.py`)
- [ ] UI accessible (`streamlit run ui.py`)
- [ ] GitHub repository ready
- [ ] GitHub Secrets configured
- [ ] Render account created
- [ ] Service IDs obtained

## 🆘 Troubleshooting

**Tests fail?**
```bash
pip install -r requirements.txt
pytest tests/ -v
```

**API won't start?**
```bash
python app.py
# Check: http://localhost:8000/health
```

**UI can't connect?**
- Check API URL in UI settings
- Ensure API is running on port 8000
- Check network connectivity

**Deployment fails?**
- Check GitHub Actions logs
- Verify GitHub Secrets are set
- Check Render deployment logs
- Review DEPLOYMENT.md

## 📞 Need Help?

1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide
2. Review [README.md](README.md) for full documentation
3. Check GitHub Actions workflow status
4. Review error logs in Render dashboard

---

**Ready? Start with:** `./setup.sh` (or `setup.bat` on Windows) 🎉
