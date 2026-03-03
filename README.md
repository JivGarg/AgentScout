# AgentScout – Deep-Research Outreach Agent

AI-powered B2B sales research tool. Input a company URL, get instant structured research and a personalized outreach email.

## Project Structure

```
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   │   ├── auth.py       # Signup, login, JWT auth
│   │   │   └── research.py   # URL analysis & history
│   │   ├── core/             # App configuration
│   │   │   ├── config.py     # Settings (env vars)
│   │   │   ├── database.py   # Async SQLAlchemy + PostgreSQL
│   │   │   └── security.py   # JWT token & password hashing
│   │   ├── models/           # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   └── search_log.py
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   │   └── schemas.py
│   │   ├── services/         # Business logic
│   │   │   ├── scraper.py    # Crawl4AI + httpx web scraper
│   │   │   └── researcher.py # LangChain AI analysis
│   │   └── main.py           # FastAPI app entry point
│   ├── requirements.txt
│   └── .env.example
├── frontend/                 # React + Vite + Tailwind
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   │   ├── Layout.jsx
│   │   │   ├── ScanningLoader.jsx
│   │   │   └── ResearchCard.jsx
│   │   ├── pages/            # Route pages
│   │   │   ├── LoginPage.jsx
│   │   │   ├── SignupPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── HistoryPage.jsx
│   │   │   └── ResultPage.jsx
│   │   ├── services/         # API client
│   │   │   └── api.js
│   │   ├── store/            # Zustand state management
│   │   │   └── authStore.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── PRD.md
```

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # Edit with your keys
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL running locally
- OpenAI API key
