# AdPatterns Backend API

FastAPI-based backend for AdPatterns advertising campaign management platform.

## 🧠 Model Integration

This backend integrates with a pre-trained ML model stored in `adpattern_final_production.csv` (located at repository root). The model provides AI-powered suggestions for ad campaigns:

- **10,000+ pre-generated ad templates** with headlines, descriptions, keywords
- **Multi-platform support:** Meta (Facebook/Instagram), Google Ads
- **Smart filtering:** By category, demographics, and user preferences
- **Real-time suggestions:** Instant results from CSV model data

### Key Endpoint: `/api/generate-suggestions`
Filters model data based on campaign parameters and returns relevant AI suggestions.

## Tech Stack

- **Framework:** FastAPI
- **Database:** MongoDB Atlas
- **Authentication:** JWT (python-jose)
- **Validation:** Pydantic v2
- **Async Driver:** Motor (async MongoDB driver)
- **Model Processing:** Pandas (CSV data filtering)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Environment configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── campaign.py      # Campaign model
│   │   └── ad_account.py    # Ad Account model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # User schemas (Pydantic)
│   │   ├── campaign.py      # Campaign schemas
│   │   └── ad_account.py    # Ad Account schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── campaigns.py     # Campaign routes
│   │   ├── ad_accounts.py   # Ad Account routes
│   │   └── users.py         # User routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication service
│   │   └── campaign.py      # Campaign service
│   └── database/
│       ├── __init__.py
│       └── mongodb.py       # MongoDB connection
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`
2. Update MongoDB Atlas connection string
3. Set your secret key and other configurations

```bash
cp .env.example .env
```

### 5. MongoDB Atlas Setup

1. Create a MongoDB Atlas account at https://www.mongodb.com/cloud/atlas
2. Create a new cluster (free tier available)
3. Create a database user with password
4. Whitelist your IP address (or use 0.0.0.0/0 for development)
5. Get your connection string and add it to `.env`

### 6. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or:

```bash
python -m uvicorn app.main:app --reload
```

### 7. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Campaigns
- `GET /api/campaigns` - Get all campaigns
- `POST /api/campaigns` - Create new campaign
- `GET /api/campaigns/{id}` - Get campaign by ID
- `PUT /api/campaigns/{id}` - Update campaign
- `DELETE /api/campaigns/{id}` - Delete campaign

### Ad Accounts
- `GET /api/ad-accounts` - Get all ad accounts
- `POST /api/ad-accounts` - Connect new ad account
- `DELETE /api/ad-accounts/{id}` - Disconnect ad account

## Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/
```

## Environment Variables

See `.env.example` for all available configuration options.
