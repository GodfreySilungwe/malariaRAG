# 📋 Deployment Checklist

## Pre-Deployment Tasks

### Local Verification
- [ ] Clone/pull latest code
- [ ] Run `./setup.sh` (or `setup.bat`)
- [ ] All tests passing: `./run_tests.sh`
- [ ] API starts: `python app.py` → `http://localhost:8000/health` returns 200
- [ ] UI loads: `streamlit run ui.py` → Opens in browser
- [ ] Chat works end-to-end locally

### Code Quality
- [ ] No linting errors: `flake8 .`
- [ ] Code formatted: `black .`
- [ ] All test cases passing
- [ ] Coverage > 70% (goal)
- [ ] No debug statements left in code

### GitHub Setup
- [ ] Repository created/pushed to GitHub
- [ ] Main branch is default branch
- [ ] `.github/workflows/test-and-deploy.yml` committed
- [ ] All files in .gitignore are not committed
- [ ] No secrets in code

## Render Setup

### Create API Token
- [ ] Go to https://dashboard.render.com/api-tokens
- [ ] Create new API token
- [ ] Copy token (you'll only see it once)
- [ ] Save it somewhere secure temporarily

### Get Service ID (After Creating First Service)
- [ ] Create first Render service manually
- [ ] Get service ID from Render dashboard (or API)
- [ ] Save it temporarily

### GitHub Secrets Configuration
- [ ] Go to Repository → Settings → Secrets and variables → Actions
- [ ] Click "New repository secret"
- [ ] Add secret `RENDER_API_KEY` with your token
- [ ] Add secret `RENDER_SERVICE_ID` with your service ID
- [ ] Verify both secrets are listed
- [ ] Do NOT click "Preview" - secrets should be masked

## Render Services Setup

### Service 1: API Backend
- [ ] Create new Web Service
- [ ] Connect to your GitHub repository
- [ ] **Name**: `malaria-rag-api`
- [ ] **Runtime**: Python
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `python app.py`
- [ ] **Plan**: Free (or Starter if preferred)
- [ ] **Environment Variable**: `PYTHON_VERSION` = `3.10`
- [ ] **Environment Variable**: `FLASK_ENV` = `production`
- [ ] Click "Create Web Service"
- [ ] Wait for first deploy (may take 5-10 minutes)
- [ ] Verify health check: `https://malaria-rag-api.onrender.com/health`

### Service 2: UI Frontend
- [ ] Go back to dashboard
- [ ] Create another Web Service
- [ ] Connect to same repository
- [ ] **Name**: `malaria-rag-ui`
- [ ] **Runtime**: Python
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `streamlit run ui.py --server.port=8501 --server.headless=true`
- [ ] **Plan**: Free
- [ ] **Environment Variable**: `PYTHON_VERSION` = `3.10`
- [ ] **Environment Variable**: `API_URL` = `https://malaria-rag-api.onrender.com`
- [ ] Click "Create Web Service"

## First Deployment

### Test the Workflow
- [ ] Make a small change to code (e.g., comment in README)
- [ ] Commit: `git add . && git commit -m "Test deployment"`
- [ ] Push: `git push origin main`
- [ ] Go to GitHub → Actions tab
- [ ] Watch workflow execute:
  - [ ] Test job starts
  - [ ] Tests run (should pass)
  - [ ] Deploy job starts (only if tests pass)
  - [ ] Deployment completes
- [ ] Check Render dashboard for updated services

### Verify Deployed Services
- [ ] API Health: `https://malaria-rag-api.onrender.com/health`
- [ ] API Works: `curl -X POST https://malaria-rag-api.onrender.com/chat -H "Content-Type: application/json" -d '{"question":"What is malaria?"}'`
- [ ] UI Loads: Visit `https://malaria-rag-ui.onrender.com`
- [ ] UI Works: Ask a question in the interface
- [ ] Sources Display: Verify sources show up correctly

## Post-Deployment

### Monitoring
- [ ] Check Render logs for errors
- [ ] Monitor GitHub Actions for failed workflows
- [ ] Set up email notifications for failed deployments
- [ ] Test health endpoints weekly

### Maintenance
- [ ] Keep dependencies updated
- [ ] Review logs regularly
- [ ] Monitor resource usage
- [ ] Plan for database persistence (future)

### Documentation
- [ ] Share deployed URLs with team
- [ ] Document API endpoints for users
- [ ] Create user guide for web UI
- [ ] Document any custom configurations

## Troubleshooting During Deployment

### If Tests Fail in GitHub Actions
- [ ] Check "Test" job log in Actions
- [ ] Identify failing test
- [ ] Fix locally and test: `./run_tests.sh`
- [ ] Commit and push fix
- [ ] Workflow will retry automatically

### If Deployment Fails
- [ ] Check "Deploy" job log in Actions
- [ ] Check Render build log in dashboard
- [ ] Common issues:
  - [ ] Missing environment variable
  - [ ] Wrong start command
  - [ ] Dependencies not installing
  - [ ] Port binding issues
- [ ] Fix and push to main again

### If Services Don't Respond
- [ ] Check Render dashboard → Active services
- [ ] Click service to view logs
- [ ] Common issues:
  - [ ] Service crashed (check logs)
  - [ ] Health check failing
  - [ ] Timeout during startup
- [ ] Try manual restart from Render dashboard

### If UI Can't Connect to API
- [ ] Verify `API_URL` environment variable is correct
- [ ] Check that API service is running
- [ ] Test API directly: `curl https://malaria-rag-api.onrender.com/health`
- [ ] Check CORS configuration in app.py (should be fine)

## Security Checklist

- [ ] No secrets in GitHub repository
- [ ] All secrets in GitHub are masked
- [ ] API keys in Render as environment variables
- [ ] CORS is properly configured (only needed origins)
- [ ] HTTPS enabled (Render provides this automatically)
- [ ] Health checks enabled
- [ ] Error messages don't expose system info

## Performance Optimization

- [ ] Monitor response times
- [ ] Check Render dashboard for resource usage
- [ ] Consider caching frequent queries (future enhancement)
- [ ] Monitor ChromaDB size growth
- [ ] Plan for database persistence (future enhancement)

## Success Criteria ✅

- [ ] GitHub Actions workflow runs on every push
- [ ] Tests pass before deployment
- [ ] Services deploy automatically to Render
- [ ] Both API and UI are accessible
- [ ] End-to-end functionality works on deployed services
- [ ] Health checks respond with 200 OK
- [ ] No errors in deployment logs

---

## Contact Points for Help

- **GitHub Actions**: Check workflow logs in Actions tab
- **Render**: Check service logs in Render dashboard
- **Documentation**: See DEPLOYMENT.md and README.md
- **Tests**: Run locally with `pytest tests/ -v`

---

**Target Deployment Date**: [Enter your date]
**Deployed By**: [Enter your name]
**Date Deployed**: [Leave blank until complete]

✅ **Mark as complete once all items are checked!**
