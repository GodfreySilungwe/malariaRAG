# 📦 Deployment Guide - MalariaAI RAG

Deploy Flask API + React Frontend to Render with automatic testing and CI/CD.

## Architecture

```
GitHub Push
    ↓
GitHub Actions (Tests)
    ↓
Render Deploy
    ↓
Live Service: https://malaria-rag-api.onrender.com
```

## Prerequisites

- GitHub account with repository
- Render account (free tier: https://render.com)
- Git configured locally

## 🚀 Deployment Steps

### Step 1: Render Setup

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub
   - Connect your GitHub account

2. **Create API Token**
   - Go to https://dashboard.render.com/api-tokens
   - Click "Create API Token"
   - Copy the token (save it safely)

### Step 2: GitHub Secrets

1. **Go to Repository Settings**
   - Repository → Settings → Secrets and variables → Actions

2. **Add Secrets**
   - `RENDER_API_KEY`: Paste your Render API token from Step 1

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Deploy Flask + React to Render"
git push origin main
```

### Step 4: Automatic Deployment

**GitHub Actions will:**
1. Run pytest (tests)
2. Run flake8 (linting)
3. Check coverage
4. Build React frontend
5. Deploy to Render (if all pass)

**Monitor at:**
- GitHub: Actions tab
- Render: Dashboard

### Step 5: Access Your App

Once deployment completes:
- **Frontend + API**: https://malaria-rag-api.onrender.com
- **Health Check**: https://malaria-rag-api.onrender.com/health

---

## 🔧 Configuration

### Environment Variables (set in Render)

| Variable | Value |
|----------|-------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `FLASK_ENV` | `production` |
| `PORT` | `5000` |

### render.yaml

The project includes `render.yaml` which automatically configures:
- Build command: Installs Python & Node dependencies, builds React
- Start command: Runs Flask on port 5000
- Health check: `/health` endpoint
- Python version: 3.10
- Free tier compatible

---

## 🧪 What Gets Tested

Before deployment, GitHub Actions runs:

```bash
# Linting
flake8 app.py malaria_rag.py model.py context.py ingest.py tests/

# Tests
pytest tests/test_malaria_rag.py -v --cov

# Check
If all pass → Deploy
If any fail → Stop deployment
```

---

## 📊 Monitoring

### Logs

1. **Render Dashboard**
   - Go to https://dashboard.render.com
   - Select service → Logs tab
   - Watch real-time logs

2. **Health Check**
   ```bash
   curl https://malaria-rag-api.onrender.com/health
   # Response: {"status": "ok"}
   ```

3. **Test API**
   ```bash
   curl -X POST https://malaria-rag-api.onrender.com/chat \
     -H "Content-Type: application/json" \
     -d '{"question":"What is malaria?"}'
   ```

---

## 🆘 Troubleshooting

### Deployment Failed

1. **Check GitHub Actions logs**
   - GitHub → Actions → Latest workflow
   - Expand failed job
   - Look for error message

2. **Common Issues**
   - `npm install` failed: Node dependencies missing
   - `pytest` failed: Tests not passing locally
   - `OPENAI_API_KEY` missing: Add to Render environment
   - Python version mismatch: Ensure Python 3.10+

### Build Takes Long

First deployment takes longer (builds React). Subsequent deploys faster (incremental builds).

### App Not Responding

1. Check health endpoint:
   ```bash
   curl https://malaria-rag-api.onrender.com/health
   ```

2. Check Render logs for errors

3. Verify environment variables set correctly

### Port Issues

Render automatically maps port `5000` to `80`/`443`. No need to change in code.

---

## 🔄 Redeploy

### Manual Redeploy

Option 1: Push to main branch:
```bash
git commit -m "Update code"
git push origin main
# GitHub Actions triggers automatically
```

Option 2: Render dashboard:
- Go to service
- Click "Manual Deploy"
- Select branch
- Click "Deploy"

---

## 🔒 Security

Best practices:

1. **Never commit secrets**
   - Use `.env.example` for templates
   - Keep `.env` in `.gitignore`
   - Add secrets via Render dashboard

2. **Use environment variables**
   ```python
   import os
   api_key = os.getenv('OPENAI_API_KEY')
   ```

3. **HTTPS enforced**
   - Render automatically uses HTTPS
   - All connections encrypted

4. **Update dependencies**
   - Regularly update `requirements.txt`
   - Check for security vulnerabilities

---

## 📈 Performance

### Cold Starts

First request after inactivity (free tier):
- Free tier: ~10-15 second startup
- Paid tier: ~1-2 second startup

### Load Times

- API response: 3-5 seconds (depends on LLM)
- Frontend load: < 1 second
- Database queries: < 100ms

### Optimization

For production:
1. Upgrade to paid tier (no cold starts)
2. Use PostgreSQL (faster queries)
3. Cache common answers
4. CDN for static files

---

## 📚 Learn More

- [Render Docs](https://render.com/docs)
- [render.yaml Reference](https://render.com/docs/blueprint-spec)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## ✅ Deployment Checklist

- [ ] Git repository initialized
- [ ] `.env.example` created (no secrets)
- [ ] GitHub secrets added (`RENDER_API_KEY`)
- [ ] `render.yaml` configured
- [ ] `requirements.txt` updated
- [ ] `frontend/package.json` exists
- [ ] All tests passing locally
- [ ] Code pushed to main branch
- [ ] GitHub Actions completed
- [ ] App accessible at Render URL
- [ ] Health endpoint responds
- [ ] API endpoint working

---

**Status**: Ready to Deploy ✅

**Version**: 2.0.0  
**Backend**: Flask (Python 3.10)  
**Frontend**: React 18  
**Deployment**: Render (Free Tier Supported)

   - **Name**: `malaria-rag-ui`
   - **Start Command**: `streamlit run ui.py --server.port=8501 --server.headless=true`
   - **Environment Variable**: `API_URL`: `https://malaria-rag-api.onrender.com`

### 3. Environment Variables

Configure these on Render dashboard:

**For API Service:**
```
FLASK_ENV=production
PYTHON_VERSION=3.10
PORT=8000
```

**For UI Service:**
```
API_URL=https://malaria-rag-api.onrender.com
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### 4. Health Checks

The application includes a `/health` endpoint that returns `{"status": "ok"}`.

Render will use this to verify the service is running.

## Continuous Deployment

The GitHub Actions workflow (`test-and-deploy.yml`) automatically:

1. **On push to main or develop**: Runs tests
2. **On successful tests**: Deploys to Render
3. **Notifications**: Posts status to GitHub

### Workflow Steps

1. **Test Phase**:
   - Installs dependencies
   - Runs linting (flake8)
   - Runs pytest suite
   - Uploads coverage reports

2. **Deploy Phase** (main branch only):
   - Triggers Render deployment via API
   - Reports success/failure

## Local Testing

### Run Tests Locally

```bash
# Activate virtual environment
source venv/Scripts/activate  # or venv\Scripts\activate on Windows

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v --cov=.
```

### Run Application Locally

**Flask API:**
```bash
python app.py
```

**Streamlit UI:**
```bash
streamlit run ui.py
```

## Deployment Checklist

- [ ] GitHub repository created and pushed
- [ ] Render account created
- [ ] GitHub secrets configured (`RENDER_API_KEY`, `RENDER_SERVICE_ID`)
- [ ] Render services created and connected
- [ ] Environment variables configured
- [ ] Tests passing locally
- [ ] First push to main branch triggers deployment
- [ ] Visit deployed URLs to verify

## Troubleshooting

### Build Fails

1. Check Render build logs in the dashboard
2. Verify all dependencies in `requirements.txt`
3. Ensure Python version is compatible
4. Check for missing environment variables

### API Not Responding

1. Verify health endpoint: `curl https://your-service.onrender.com/health`
2. Check Render logs for errors
3. Verify API is listening on correct port
4. Check CORS configuration

### Streamlit Issues

1. Verify `API_URL` environment variable is set correctly
2. Check Streamlit logs for connection errors
3. Ensure Flask API is running and accessible

### Tests Failing in CI

1. Review GitHub Actions logs
2. Run tests locally to reproduce
3. Check for environment-specific issues
4. Update tests if needed

## Performance Tips

1. Use Render's Postgres database for persistence
2. Configure caching for LLM responses
3. Monitor resource usage in Render dashboard
4. Consider upgrading from free to paid plan for production

## Security

1. Keep API keys in GitHub secrets only
2. Use environment variables for sensitive data
3. Enable CORS carefully
4. Run health checks regularly
5. Monitor deployment logs

## Next Steps

1. Add more comprehensive tests
2. Set up database for ChromaDB persistence
3. Implement rate limiting
4. Add authentication/API keys
5. Set up monitoring and alerts

---

For more information:
- [Render Documentation](https://render.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
