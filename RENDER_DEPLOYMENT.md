# Deploy Flask Portfolio to Render ✨

## Pre-Deployment Checklist

- ✅ Created `Procfile` (tells Render how to run your app)
- ✅ Created `render.yaml` (Render configuration)
- ✅ Updated `requirements.txt` with `gunicorn` and `python-dotenv`
- ✅ Updated `app.py` to use environment variables
- ✅ Created `.env.example` template

## Step-by-Step Deployment Guide

### Step 1: Push to GitHub

```bash
# Initialize git repo (if not already done)
git init
git add .
git commit -m "Ready for Render deployment"

# Create a new repository on GitHub.com
# Then push your code:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/flask-portfolio.git
git push -u origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Sign Up"
3. Connect your GitHub account
4. Authorize Render to access your repositories

### Step 3: Deploy Your App

1. Click **"New +"** → **"Web Service"**
2. Select your `flask-portfolio` repository
3. Fill in the settings:
   - **Name:** `flask-portfolio` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free (or Starter for better performance)

### Step 4: Set Environment Variables

In the Render dashboard for your service:

1. Go to **"Environment"** tab
2. Add these variables:
   ```
   SECRET_KEY = (click "Generate" to auto-generate)
   FLASK_ENV = production
   PYTHON_VERSION = 3.11.0
   ```

3. **Important:** Update `SECRET_KEY` with a strong random string:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Build your app
   - Deploy it live

3. Wait for the build to complete (2-5 minutes)
4. Your app will be live at: `https://flask-portfolio.onrender.com`

---

## File Descriptions

| File | Purpose |
|------|---------|
| `Procfile` | Tells Render how to run the app (uses gunicorn) |
| `render.yaml` | Infrastructure as Code - defines all Render settings |
| `requirements.txt` | Updated with `gunicorn` and `python-dotenv` |
| `.env.example` | Template for environment variables |
| `app.py` | Updated to read from environment variables |

---

## Production Checklist

Before deploying, ensure:

- ✅ All secret keys are in environment variables (not in code)
- ✅ `DEBUG = False` in production
- ✅ Database/file uploads configured for persistence
- ✅ Static files properly linked
- ✅ Error handlers configured
- ✅ CORS settings if using API

---

## Troubleshooting

### App crashes immediately after deploy?
- Check logs: Click service → "Logs" tab
- Ensure `Procfile` is in root directory
- Verify all dependencies in `requirements.txt`

### Static files not loading?
```python
# Flask automatically serves from static/ folder
# Ensure your templates use:
{{ url_for('static', filename='css/style.css') }}
```

### 502 Bad Gateway error?
- Wait a few minutes for deployment to complete
- Check that `gunicorn app:app` command is correct
- Verify app runs locally: `python app.py`

### Can't upload files?
- File uploads go to `/tmp` on Render's free tier (ephemeral)
- For persistent storage, use Render Disks or external storage (AWS S3)

---

## Custom Domain (Optional)

1. Go to your service settings → **"Custom Domain"**
2. Add your domain (e.g., `myportfolio.com`)
3. Follow DNS instructions
4. SSL certificate auto-provisioned

---

## Monitoring & Logs

- **Logs:** Service → "Logs" tab (real-time updates)
- **Metrics:** Service → "Metrics" tab
- **Restart:** Service → "Manual Actions" → "Restart"

---

## Update Your App

After deployment, any changes are simple:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render automatically redeploys! 🚀

---

## Need Help?

- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com
- Contact support in Render dashboard
