# Railway Deployment

## Service Configuration

Railway builds the repository with the root `Dockerfile` and starts the container with:

```text
python app.py
```

The application reads Railway's injected `PORT` value. Do not hard-code a Railway port in the service settings.

Set this variable in **Railway -> Service -> Variables**:

```text
OPENROUTER_API_KEY=your-rotated-key
FLASK_ENV=production
```

Railway provides the `PORT` variable automatically.

## GitHub Actions Deployment

The workflow at `.github/workflows/test-and-deploy.yml` runs tests for pushes and pull requests. It deploys only for a push to `main`, after the `test` job succeeds.

Add these repository secrets in **GitHub -> Settings -> Secrets and variables -> Actions**:

```text
RAILWAY_TOKEN
RAILWAY_PROJECT_ID
RAILWAY_ENVIRONMENT_ID
RAILWAY_SERVICE_ID
```

The workflow installs the Railway CLI and runs `railway up --ci` with those identifiers.

To avoid deploying before tests finish, disable Railway's separate automatic GitHub deployment trigger if one is enabled. Keep the Railway service connected to the repository so the CLI deployment can build the current commit.

## Deploying

```bash
git add .
git commit -m "Describe the change"
git push origin main
```

Then monitor the GitHub Actions workflow and Railway deployment logs.

## Verification

The deployed service should respond to:

```text
https://malariarag-production.up.railway.app/health
```

Expected response:

```json
{"status":"ok"}
```

Example API request:

```bash
curl -X POST https://malariarag-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What are the preventive measures for malaria?"}'
```

Never commit `.env`, API keys, Railway tokens, or other credentials.
