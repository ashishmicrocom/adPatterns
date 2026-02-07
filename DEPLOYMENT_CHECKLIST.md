# 🚀 Quick Deployment Checklist

## Before You Start

- [ ] Code pushed to GitHub
- [ ] MongoDB Atlas account created
- [ ] Vercel account ready
- [ ] Railway account ready

---

## 🚂 Railway Backend Deployment

1. **Create Project**
   - [ ] Connect GitHub repo
   - [ ] Set root directory to `backend`

2. **Environment Variables**
   - [ ] MONGODB_URL (from MongoDB Atlas)
   - [ ] SECRET_KEY (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
   - [ ] FRONTEND_URL (add later after Vercel)
   - [ ] ALLOWED_ORIGINS (add later after Vercel)
   - [ ] DEBUG=False

3. **Verify**
   - [ ] CSV file exists in repo root
   - [ ] Deployment successful
   - [ ] Copy Railway URL: `_______________________`
   - [ ] Test health endpoint: `https://your-url/health`
   - [ ] Test model stats: `https://your-url/api/model-stats`

---

## ☁️ Vercel Frontend Deployment

1. **Create Project**
   - [ ] Import GitHub repo
   - [ ] Set root directory to `frontend`
   - [ ] Framework: Next.js (auto-detected)

2. **Environment Variables**
   - [ ] NEXT_PUBLIC_API_URL (your Railway URL)

3. **Verify**
   - [ ] Deployment successful
   - [ ] Copy Vercel URL: `_______________________`
   - [ ] Open in browser and test

---

## 🔄 Update Backend CORS

- [ ] Go back to Railway → Variables
- [ ] Update FRONTEND_URL with Vercel URL
- [ ] Update ALLOWED_ORIGINS with Vercel URL
- [ ] Wait for Railway to redeploy

---

## 🗄️ MongoDB Atlas Setup

- [ ] Create free cluster
- [ ] Create database user
- [ ] Add network access: `0.0.0.0/0`
- [ ] Get connection string
- [ ] Add to Railway MONGODB_URL

---

## ✅ Final Tests

**Backend:**
- [ ] Health check works: `GET /health`
- [ ] API docs accessible: `GET /docs`
- [ ] Model stats loads: `GET /api/model-stats`
- [ ] Generate suggestions works: `POST /api/generate-suggestions`

**Frontend:**
- [ ] Homepage loads
- [ ] Can navigate to campaign creation
- [ ] AI suggestions load (from model)
- [ ] Can login/register

**Integration:**
- [ ] Frontend can call backend
- [ ] No CORS errors
- [ ] Model data loads correctly

---

## 📝 URLs to Save

```
Frontend (Vercel):  https://___________________________
Backend (Railway):  https://___________________________
API Docs:          https://___________________________/docs
MongoDB Atlas:     https://cloud.mongodb.com
```

---

## 🎉 Success Criteria

✅ Frontend loads without errors
✅ Backend health check returns `{"status": "healthy"}`
✅ Model stats shows CSV data loaded
✅ Can generate AI suggestions
✅ CORS configured correctly
✅ Database connected

---

## 🚨 Common Issues

**"Model CSV not found"**
→ Ensure `adpattern_final_production.csv` is in repo root

**CORS errors**
→ Update ALLOWED_ORIGINS in Railway with your Vercel URL

**Database connection failed**
→ Check MONGODB_URL and MongoDB network access

**API calls fail**
→ Verify NEXT_PUBLIC_API_URL in Vercel

---

## 📞 Need Help?

- Railway Logs: Check deployment logs for errors
- Vercel Logs: Check build logs for issues
- MongoDB: Verify connection string and credentials

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
