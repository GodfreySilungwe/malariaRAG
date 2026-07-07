# Running Multiple UIs

MalariaAI supports three different user interfaces that can run simultaneously:

1. **JavaScript Web UI** - Modern web app (Node.js/Express)
2. **Streamlit UI** - Python-based UI (Streamlit)
3. **REST API** - Direct API access (Flask)

## Quick Comparison

| Feature | Web UI | Streamlit | API Only |
|---------|--------|-----------|----------|
| Technology | JavaScript/HTML | Python/Streamlit | Flask/Python |
| Port | 3000 | 8501 | 8000 |
| Setup | `npm start` | `streamlit run ui.py` | `python app.py` |
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Customization | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Deployment | Easy | Medium | Medium |
| Learning Curve | Medium | Low | High |

## Setup All Services

### Option 1: Individual Terminals (Recommended for Development)

**Terminal 1 - Flask API Backend:**
```bash
python app.py
# Runs on http://localhost:8000
```

**Terminal 2 - JavaScript Web UI:**
```bash
npm start
# Runs on http://localhost:3000
```

**Terminal 3 - Streamlit UI (Optional):**
```bash
streamlit run ui.py
# Runs on http://localhost:8501
```

All can run simultaneously! Each terminal shows its own logs.

### Option 2: Docker Compose (Production)

```bash
docker-compose up
```

This starts all three services:
- API: http://localhost:8000
- Web UI: http://localhost:3000
- Streamlit: http://localhost:8501

Stop with: `Ctrl+C` then `docker-compose down`

### Option 3: Selective Services

Start only the services you need:

```bash
# Just API
python app.py

# Just Web UI (connects to remote API)
API_URL=https://remote-api.example.com npm start

# Just API + Web UI
docker-compose up api web
```

## Service Communication

```
┌─────────────────────────────────────────────────────┐
│                   User Browsers                     │
├─────────────────────────────────────────────────────┤
│  Web UI (3000)  Streamlit (8501)  API (8000)       │
├─────────────────────────────────────────────────────┤
│         ↓              ↓              ↓             │
│   Express.js      Streamlit        Flask API       │
│   Node.js         Python            Python         │
├─────────────────────────────────────────────────────┤
│              All access Flask API on 8000           │
│     (API can run without UIs, UIs need API)        │
└─────────────────────────────────────────────────────┘
```

## Configuration

### Environment Variables

Each service uses its own configuration:

**Flask API** (`.env`):
```env
FLASK_ENV=development
PORT=8000
OPENAI_API_KEY=your_key
```

**Web UI** (`.env`):
```env
NODE_ENV=development
PORT=3000
API_URL=http://localhost:8000
```

**Streamlit** (`.env`):
```env
STREAMLIT_SERVER_PORT=8501
API_URL=http://localhost:8000
```

## Using Each UI

### Web UI (JavaScript)

**Access:** http://localhost:3000

**Features:**
- Modern, responsive design
- Real-time chat
- Source attribution
- Settings panel
- Health status indicator

**Start:** `npm start`

**Documentation:** See [QUICKSTART_WEB.md](QUICKSTART_WEB.md) and [JAVASCRIPT_UI.md](JAVASCRIPT_UI.md)

### Streamlit UI (Python)

**Access:** http://localhost:8501

**Features:**
- Python-based
- Interactive widgets
- Data visualization
- Quick to build

**Start:** `streamlit run ui.py`

**Documentation:** See [QUICKSTART.md](QUICKSTART.md)

### REST API (Direct Access)

**Access:** http://localhost:8000

**Endpoints:**
- `GET /` - Welcome
- `GET /health` - Health check
- `POST /chat` - Send question

**Testing:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What is malaria?"}'
```

## Switching Between UIs

You can use all three simultaneously! In your browser:

1. **Web UI**: http://localhost:3000
2. **Streamlit**: http://localhost:8501
3. **API Direct**: http://localhost:8000/health

Just open different tabs for each.

## Deployment Scenarios

### Scenario 1: Web UI Only
- Deploy JavaScript Web UI to Render
- Connect to hosted Flask API
- Lightest weight, lowest cost

**Render Services:**
- malaria-rag-api (Python)
- malaria-rag-web (Node.js)

### Scenario 2: Web UI + Streamlit
- Deploy both UIs to Render
- Share same Flask API backend
- Maximum flexibility

**Render Services:**
- malaria-rag-api (Python)
- malaria-rag-web (Node.js)
- malaria-rag-ui-streamlit (Python)

### Scenario 3: API Only
- Deploy just Flask API to Render
- Use external UI or custom client
- Minimum deployment

**Render Services:**
- malaria-rag-api (Python only)

## Performance Comparison

### API Response Times (local, no network latency)

```
Chat Query Response:
- Web UI:    ~5-15 seconds (depends on API)
- Streamlit: ~5-15 seconds (depends on API)
- Direct:    ~5-15 seconds (same backend)
```

### Server Overhead

```
Web UI:    ~50MB memory, minimal CPU
Streamlit: ~100MB memory, higher CPU
API:       ~200MB memory, varies with queries
```

### Startup Times

```
Web UI:    < 1 second
Streamlit: 5-10 seconds
API:       5-10 seconds
```

## Troubleshooting Multiple Services

### Port Conflicts

**Problem:** `Address already in use`

**Solution:**
```bash
# Change port
PORT=3001 npm start        # Web UI on 3001
STREAMLIT_SERVER_PORT=8502 streamlit run ui.py  # Streamlit on 8502
```

### Services Can't Connect

**Problem:** Web UI can't reach API

**Solution:**
1. Verify API is running: `curl http://localhost:8000/health`
2. Update API_URL in settings or `.env`
3. Check firewall settings

### Logs Getting Mixed

**Solution:** Use separate terminals for each service:

```bash
# Terminal 1
python app.py        # API logs

# Terminal 2
npm start           # Web UI logs

# Terminal 3
streamlit run ui.py # Streamlit logs
```

## Docker Compose Advanced

### Start specific services

```bash
# Just API
docker-compose up api

# API + Web UI
docker-compose up api web

# All services
docker-compose up
```

### Development with hot-reload

```bash
# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Database Persistence

ChromaDB data persists in `chromadb/` volume between runs.

Clear with:
```bash
docker-compose down -v
```

## Monitoring All Services

### Health Check Script

```bash
#!/bin/bash

echo "🔍 Checking all services..."
echo ""

echo "🔌 API Backend:"
curl -s http://localhost:8000/health | jq . || echo "❌ Not running"

echo ""
echo "🌐 Web UI:"
curl -s http://localhost:3000/api/health | jq . || echo "❌ Not running"

echo ""
echo "📊 Streamlit:"
curl -s http://localhost:8501/_stcore/health | jq . || echo "❌ Not running"

echo ""
echo "✅ Check complete!"
```

## Production Deployment

### Recommended Setup

1. **API**: Always running on Render (Python service)
2. **Web UI**: Recommended for production (Node.js, lightweight)
3. **Streamlit**: Optional (for internal use)

### Render Configuration

See `render.yaml`:

```yaml
services:
  - name: malaria-rag-api          # Python, 8000
  - name: malaria-rag-web          # Node.js, 3000
  - name: malaria-rag-ui-streamlit # Python, 8501 (optional)
```

All services connect to same API backend.

## Summary

| Task | Command |
|------|---------|
| Start all (dev) | Terminal 1: `python app.py` → Terminal 2: `npm start` → Terminal 3: `streamlit run ui.py` |
| Start all (docker) | `docker-compose up` |
| Start Web UI only | `npm start` |
| Start Streamlit only | `streamlit run ui.py` |
| Start API only | `python app.py` |
| Check all services | `curl localhost:8000/health` & `curl localhost:3000/api/health` |
| Deploy to Render | Push to main, GitHub Actions deploys all services |

---

**Need Help?**
- Web UI: See [QUICKSTART_WEB.md](QUICKSTART_WEB.md)
- Streamlit: See [QUICKSTART.md](QUICKSTART.md)
- Deployment: See [DEPLOYMENT.md](DEPLOYMENT.md)
- JavaScript UI Details: See [JAVASCRIPT_UI.md](JAVASCRIPT_UI.md)
