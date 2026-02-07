# AdPatterns - AI-Powered Advertising Campaign Platform

> Deploy your campaigns smarter with AI-driven suggestions powered by machine learning

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with API URL
npm run dev
```

## 📦 Project Structure

```
adPatterns/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── config/         # Settings & configuration
│   │   ├── database/       # MongoDB connection
│   │   ├── routes/         # API endpoints
│   │   ├── schemas/        # Pydantic models
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   ├── Procfile           # Railway deployment
│   └── .env.example       # Environment template
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/    # React components
│   │   ├── config/        # Configuration (API URLs)
│   │   └── lib/           # Utilities
│   ├── package.json
│   ├── vercel.json        # Vercel deployment
│   └── .env.example       # Environment template
│
├── adpattern_final_production.csv  # ML Model data
└── DEPLOYMENT.md          # Deployment guide
```

## 🎯 Features

- ✅ **AI Suggestions** - ML-powered headlines, descriptions, keywords
- ✅ **Multi-Platform** - Meta (Facebook/Instagram), Google Ads support
- ✅ **Campaign Management** - Create, review, and publish campaigns
- ✅ **Audience Targeting** - Age, gender, location-based filtering
- ✅ **Real-time Preview** - See your ads before publishing
- ✅ **Authentication** - Secure user accounts with JWT

## 🧠 Model Integration

The application uses a pre-trained model stored in `adpattern_final_production.csv`. The model data includes:

- **10,000+ generated ad templates** across multiple categories
- **Demographic targeting** (age, gender, location)
- **Platform-specific** content (Meta, Google)
- **Keywords & image prompts** for each suggestion

The backend (`/api/generate-suggestions`) filters this data based on:
- Product category
- Target audience demographics
- Selected platform
- Budget and objectives

## 🔧 Technology Stack

**Backend:**
- FastAPI (Python web framework)
- MongoDB (Database)
- Pandas (Model data processing)
- JWT (Authentication)

**Frontend:**
- Next.js 16 (React framework)
- TypeScript
- Tailwind CSS
- Framer Motion (Animations)

**Deployment:**
- Railway (Backend)
- Vercel (Frontend)
- MongoDB Atlas (Database)

## 📚 API Documentation

Once deployed, access interactive API docs:
- Swagger UI: `https://your-backend.railway.app/docs`
- ReDoc: `https://your-backend.railway.app/redoc`

### Key Endpoints:

```
POST /api/auth/register          - Create new account
POST /api/auth/login/json        - User login
POST /api/generate-suggestions   - Get AI suggestions from model
GET  /api/model-stats            - View model statistics
POST /api/campaigns              - Create campaign
POST /api/campaigns/{id}/publish - Publish campaign
```

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to:
- Railway (Backend + Model)
- Vercel (Frontend)
- MongoDB Atlas (Database)

## 🔐 Environment Variables

### Backend (.env)
```bash
MONGODB_URL=mongodb+srv://...
SECRET_KEY=your_secret_key
FRONTEND_URL=https://your-frontend.vercel.app
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

See `.env.example` files for complete configuration.

## 🧪 Testing

**Backend Health Check:**
```bash
curl http://localhost:8000/health
```

**Model Stats:**
```bash
curl http://localhost:8000/api/model-stats
```

**Generate Suggestions:**
```bash
curl -X POST http://localhost:8000/api/generate-suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Clothing",
    "gender": "Male",
    "platform": "Meta",
    "age_min": 18,
    "age_max": 35
  }'
```

## 📊 Model Data Structure

The CSV file (`adpattern_final_production.csv`) contains:

| Column | Description |
|--------|-------------|
| User_ID | Unique user identifier |
| Category | Product category (Clothing, Electronics, etc.) |
| Platform | Ad platform (Meta, Google) |
| Gender | Target gender (Male, Female, All) |
| Age_Min, Age_Max | Age range |
| Locations | Target locations (comma-separated) |
| Headline | Generated ad headline |
| Ad_Description | Generated ad copy |
| Keyword | SEO keywords |
| Image_Prompt | AI image generation prompt |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is proprietary software.

## 🆘 Support

For issues or questions:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
2. Review API docs at `/docs` endpoint
3. Check Railway/Vercel logs for errors

---

**Built with ❤️ for smarter advertising campaigns**
