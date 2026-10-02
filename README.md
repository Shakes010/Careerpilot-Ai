# CareerPilot AI — Full-Stack Working Platform

> **MCA Final Year Capstone Project — Team 4**  
> **Team Members:** Sen Shaji, Abel Mathew Bose, Sidharth K A, K M Meenakshi  
> **Architecture:** Decoupled FastAPI Backend + Vue 3 Frontend + PostgreSQL

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.11–3.14)
- **Node.js 18+** & npm
- **PostgreSQL** running locally on port 5432 (`careerpilot` database with user `postgres`/`postgres`)

---

### 2. Run Backend (FastAPI)

```bash
# Navigate to the backend folder
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server (runs on http://127.0.0.1:8000)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **API Documentation & Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative startup script:** `python run_backend.py` from repository root.

---

### 3. Run Frontend (Vue 3 + Vite)

```bash
# Navigate to the frontend folder
cd frontend

# Install packages
npm install

# Start Vite dev server (runs on http://127.0.0.1:5180)
npm run dev -- --host 127.0.0.1 --port 5180
```

- **Web Application URL:** [http://127.0.0.1:5180](http://127.0.0.1:5180)

---

## 🔑 Login Accounts (Default Seed)

| Role | Email | Password | Access / Features |
| :--- | :--- | :--- | :--- |
| **Student (Pro)** | `student@careerpilot.ai` | `student123` | AI Resume Studio, Career Passport, Assessments, Opportunity Radar |
| **Recruiter** | `recruiter@careerpilot.ai` | `password123` | Post Jobs, Candidate Comparison, Match Explainability, Cascade Deletion |
| **Admin** | `admin@careerpilot.ai` | `admin123` | Admin Console, Flagged Review Queue, User Management |

---

## 📦 Project Architecture & Modules

```
Careerpilot-Ai/
├── backend/
│   ├── app/
│   │   ├── config.py           # Configuration & App Settings
│   │   ├── database.py         # SQLAlchemy Engine & Session
│   │   ├── init_db.py          # Database initialization & seeding
│   │   ├── main.py             # FastAPI entrypoint & router registrations
│   │   ├── migrate_columns.py  # Column migration utility
│   │   ├── models.py           # SQLAlchemy ORM Models
│   │   ├── routers/            # Modular API endpoints
│   │   │   ├── admin_router.py
│   │   │   ├── assessments_router.py
│   │   │   ├── auth_router.py
│   │   │   ├── opportunities_router.py
│   │   │   ├── payments_router.py
│   │   │   ├── profile_router.py
│   │   │   ├── projects_router.py
│   │   │   ├── recruiter_router.py
│   │   │   └── skills_router.py
│   │   ├── schemas/            # Pydantic schemas
│   │   └── services/           # Business logic & AI algorithms
│   │       ├── ai_matcher.py          # Semantic skill matching (MiniLM embeddings)
│   │       ├── auth_service.py        # JWT & bcrypt verification
│   │       ├── code_executor.py       # Multi-language code evaluation
│   │       ├── judge0_service.py      # Code execution integration
│   │       ├── razorpay_service.py    # HMAC-SHA256 signature verification
│   │       ├── resume_parser.py       # PDF extraction & ATS scoring
│   │       └── trust_meter_service.py # Noisy-OR probabilistic evidence aggregation
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable navigation & UI elements
│   │   ├── router/             # Vue Router configuration
│   │   ├── services/           # API fetch helpers
│   │   ├── store/              # Pinia auth store
│   │   ├── views/              # Full page views
│   │   │   ├── AdminView.vue
│   │   │   ├── AnalyticsView.vue
│   │   │   ├── ApplicationsView.vue
│   │   │   ├── AssessmentsView.vue
│   │   │   ├── BillingView.vue
│   │   │   ├── DashboardView.vue
│   │   │   ├── LandingView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── OpportunitiesView.vue
│   │   │   ├── PassportView.vue
│   │   │   ├── ProjectsView.vue
│   │   │   ├── RecruiterView.vue
│   │   │   └── SkillsView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 👥 Module Distribution by Team Member

- **Sen Shaji:** Lead Full-Stack Architecture, AI Resume Studio, Anti-Cheat Proctoring Pipeline & Admin Review Queue.
- **Abel Mathew Bose:** Database & Schema Modeling, Skill Evidence Ledger, Recruiter Candidate Search & Filtering.
- **Sidharth K A:** Razorpay Payments, Commercial Billing, Subscriptions, GST Invoices, Layout & CSS Theme Palettes.
- **K M Meenakshi:** NLP Resume Parsing, Skill Trust Score Formulation, Opportunity Radar Telemetry, Automated Test Suites.
