# AdPatterns Deployment Guide

This guide will help you deploy your **AdPatterns** application with:
- **Frontend** → Vercel
- **Backend** → Railway
- **Model Data** → CSV file included in backend deployment

---

## 📋 Prerequisites

Before deploying, ensure you have:

1. ✅ GitHub repository with your code pushed
2. ✅ MongoDB Atlas account (for database) - [Get Free Tier](https://www.mongodb.com/cloud/atlas/register)
3. ✅ Vercel account - [Sign up free](https://vercel.com/signup)
4. ✅ Railway account - [Sign up free](https://railway.app/)

---

## 🚂 Part 1: Deploy Backend to Railway

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app/) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your **adPatterns** repository
5. Set the **root directory** to `backend`

### Step 2: Configure Environment Variables

In your Railway project dashboard, go to **Variables** tab and add:

```bash
# MongoDB Configuration (REQUIRED)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=adpatterns_db

# Security (REQUIRED - Generate a strong key)
SECRET_KEY=your_secret_key_here_min_32_chars

# CORS (Update after Vercel deployment)
FRONTEND_URL=https://your-frontend.vercel.app
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# Application Settings
DEBUG=False
HOST=0.0.0.0
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Meta & Google Ads API credentials
META_APP_ID=
META_APP_SECRET=
GOOGLE_ADS_CLIENT_ID=
GOOGLE_ADS_CLIENT_SECRET=
```

**🔑 To generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Verify Model Data

The `adpattern_final_production.csv` file **MUST** be in your GitHub repository root. Railway will include it in the deployment automatically.

### Step 4: Deploy

1. Railway will automatically deploy when you connect the repo
2. Wait for deployment to complete (~2-5 minutes)
3. Copy your Railway app URL (e.g., `https://adpatterns-backend-production.up.railway.app`)
4. Test your backend: `https://your-railway-url/health`

---

## ☁️ Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Project

1. Go to [vercel.com](https://vercel.com/) and sign in
2. Click **"Add New Project"**
3. Import your **adPatterns** GitHub repository
4. Set **Root Directory** to `frontend`
5. Framework Preset: **Next.js** (should auto-detect)

### Step 2: Configure Environment Variables

In Vercel project settings → **Environment Variables**, add:

```bash
NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app
```

**Replace** `your-railway-backend-url.up.railway.app` with your actual Railway URL from Part 1.

### Step 3: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (~3-5 minutes)
3. You'll get a Vercel URL like: `https://adpatterns-frontend-xyz.vercel.app`

### Step 4: Update Backend CORS

Go back to **Railway** → **Variables** and update:

```bash
FRONTEND_URL=https://your-actual-vercel-url.vercel.app
ALLOWED_ORIGINS=https://your-actual-vercel-url.vercel.app,http://localhost:3000
```

Then redeploy your Railway backend (it will automatically redeploy on env variable change).

---

## 🗄️ Part 3: Setup MongoDB Atlas

### Step 1: Create Database

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user with password
4. Add IP Address `0.0.0.0/0` to Network Access (or use Railway's IP)

### Step 2: Get Connection String

1. Click **"Connect"** → **"Connect your application"**
2. Copy the connection string: 
   ```
   mongodb+srv://username:password@cluster.mongodb.net/
   ```
3. Replace `username` and `password` with your database credentials
4. Add this to Railway's `MONGODB_URL` environment variable

---

## 🧪 Testing Your Deployment

### Test Backend

```bash
# Health check
curl https://your-railway-url/health

# API documentation
https://your-railway-url/docs

# Model stats endpoint
curl https://your-railway-url/api/model-stats
```

### Test Frontend

1. Open your Vercel URL in a browser
2. Try creating a campaign
3. Check that AI suggestions are loading (they come from your model CSV)

---

## 🔧 Local Development Setup

### Backend (Local)

```bash
cd backend

# Create .env file (copy from .env.example)
cp .env.example .env

# Edit .env with your credentials
# MONGODB_URL=your_local_or_atlas_url
# SECRET_KEY=your_secret_key
# FRONTEND_URL=http://localhost:3000

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

### Frontend (Local)

```bash
cd frontend

# Create .env.local file
cp .env.local.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Install dependencies
npm install

# Run development server
npm run dev
```

---

## 📊 Verifying Model Integration

Your model data (`adpattern_final_production.csv`) is automatically loaded by the backend.

**To verify it's working:**

1. Backend logs will show: `🚀 Starting AdPatterns API...`
2. Check model stats: `GET /api/model-stats`
3. Generate suggestions with parameters matching your CSV structure:
   ```json
   POST /api/generate-suggestions
   {
     "category": "Clothing",
     "gender": "Male",
     "platform": "Meta"
   }
   ```

**Important:** The CSV file contains your trained model data with columns:
- User_ID, Category, Platform, Gender, Age_Min, Age_Max
- Headline, Ad_Description, Keyword, Image_Prompt
- Price, Locations

The backend filters this data based on user inputs to provide relevant suggestions.

---

## 🚨 Troubleshooting

### Backend Issues

**Problem:** Model data not found
- **Solution:** Ensure `adpattern_final_production.csv` is in your GitHub repo root
- Check Railway logs for CSV path errors

**Problem:** Database connection fails
- **Solution:** Verify MONGODB_URL in Railway environment variables
- Check MongoDB Atlas network access settings

**Problem:** CORS errors
- **Solution:** Update ALLOWED_ORIGINS in Railway with your Vercel URL

### Frontend Issues

**Problem:** API calls fail with 404
- **Solution:** Verify NEXT_PUBLIC_API_URL in Vercel environment variables
- Ensure Railway backend is deployed and running

**Problem:** Build fails
- **Solution:** Check Next.js build logs in Vercel
- Ensure all dependencies are in package.json

---

## 🔄 Updating Your Deployment

### Update Backend
```bash
git add backend/
git commit -m "Update backend"
git push
```
Railway auto-deploys on push.

### Update Frontend
```bash
git add frontend/
git commit -m "Update frontend"
git push
```
Vercel auto-deploys on push.

### Update Model Data
```bash
# Update CSV file
git add adpattern_final_production.csv
git commit -m "Update model data"
git push
```
Railway will redeploy with new data.

---

## 📝 Environment Variables Summary

### Railway (Backend)
| Variable | Required | Description |
|----------|----------|-------------|
| MONGODB_URL | ✅ Yes | MongoDB connection string |
| SECRET_KEY | ✅ Yes | JWT secret (32+ chars) |
| FRONTEND_URL | ✅ Yes | Your Vercel URL |
| ALLOWED_ORIGINS | ✅ Yes | Comma-separated allowed origins |
| DEBUG | No | Set to False for production |

### Vercel (Frontend)
| Variable | Required | Description |
|----------|----------|-------------|
| NEXT_PUBLIC_API_URL | ✅ Yes | Your Railway backend URL |

---

## 🎉 Success!

Your AdPatterns application is now deployed and the model is integrated!

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://your-app.railway.app`
- **API Docs:** `https://your-app.railway.app/docs`

The AI suggestions are powered by your CSV model data, automatically filtered based on user inputs!

---

## 💡 Tips

1. **Custom Domain:** Add your custom domain in Vercel/Railway settings
2. **Monitoring:** Check Railway logs for backend issues
3. **Updates:** Just push to GitHub - auto-deployment is enabled
4. **Costs:** Both platforms have free tiers; monitor usage
5. **Model Updates:** Update CSV and push to GitHub to update model data

---

**Need help?** Check the Railway and Vercel documentation or create an issue in your repository.
