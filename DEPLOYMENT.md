# Streamlit Cloud Deployment Guide

## 🚀 Deploy Kirloskar RAG Bot to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Push your code to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Kirloskar RAG Bot"
   git branch -M main
   git remote add origin https://github.com/yourusername/kirloskar-bot.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `streamlit_ragbot.py`
6. Click "Deploy"

### Step 3: Configure Secrets
In your Streamlit Cloud app dashboard:

1. Go to "Settings" → "Secrets"
2. Add the following secrets:

```toml
[chromadb]
api_key = "YOUR_CHROMADB_API_KEY"
tenant = "YOUR_CHROMADB_TENANT"
database = "YOUR_CHROMADB_DATABASE"

[azure_openai]
endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
deployment = "YOUR_DEPLOYMENT_NAME"
api_key = "YOUR_AZURE_OPENAI_API_KEY"
api_version = "2025-01-01-preview"
```

3. Click "Save"

### Step 4: Verify Deployment
- Your app will automatically redeploy with the new secrets
- Test the functionality by asking questions about Kirloskar
- Share the public URL with your team

## 📁 Files Required for Deployment
- `streamlit_ragbot.py` - Main application
- `requirements.txt` - Dependencies
- `.streamlit/config.toml` - App configuration
- `.streamlit/secrets.toml` - Local secrets (for development only)

## 🔒 Security Notes
- Never commit secrets to your repository
- The `.streamlit/secrets.toml` file should be in `.gitignore`
- Use Streamlit Cloud's secrets management for production credentials

## 🎯 Post-Deployment
Your RAG bot will be available at:
`https://[your-app-name].streamlit.app`

The bot will automatically connect to your ChromaDB knowledge base and provide AI-powered responses about Kirloskar using Azure OpenAI.
