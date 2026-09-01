# CareerPilot AI — Recruiter Module (Phase 1)

> **MCA Final Year Group Project**  
> **Developer:** Sensha (Responsibility: Recruiter Module + Payment & Subscriptions)  
> **Current Phase:** Phase 1 Only (Recruiter Authentication, Company Profile, Dashboard & Job Management)

---

## 📌 Project Overview & Scope Isolation

CareerPilot AI is an AI-powered career development platform connecting **Students**, **Recruiters**, and **Administrators**.

This repository contains the **isolated, modular Phase 1 Recruiter Module**. In accordance with team collaboration rules, this module is developed independently without overwriting or interfering with other team members' modules (*Student Profile/Career Passport*, *Skill Verification*, *Project Collaboration/Admin*).

### ✅ Phase 1 Implemented Features
1. **Recruiter Authentication**: Registration, Login, JWT token generation, Protected routes, Logout.
2. **Company Management**: Initial company creation, Company profile view & edit, Verification status tracking (`PENDING`, `VERIFIED`, `REJECTED`).
3. **Recruiter Dashboard**: Statistics cards (Active Jobs, Draft Jobs, Total Jobs, Company Status), Quick action buttons, Recent jobs widget.
4. **Job Management**: Job creation, Saving drafts, Job preview before publishing, Editing jobs, Status transitions (`DRAFT` → `PUBLISHED` → `PAUSED` → `CLOSED`), Draft job deletion, Job search, and multi-parameter filtering.
5. **Business Rule Enforcement**:
   - Recruiters from `PENDING` or `REJECTED` companies can draft and edit jobs, but **cannot publish jobs** until company status is `VERIFIED`.
   - Cross-company ownership protection (Recruiter A is strictly forbidden from viewing or modifying Recruiter B's company jobs).
   - Validation rules (Experience range, Salary range, Future deadline date, Required skills).
6. **Testing & Docs**: 100% passing Pytest suite for backend auth, role security, job lifecycle, and ownership protection. OpenAPI Swagger documentation available at `/docs`.

---

## 🚫 Phase 2 Deferred Scope (Not in Phase 1)
The following features belong strictly to Phase 2 and are **not** implemented in this phase:
- Candidate Search & Candidate Comparison
- Application Pipeline & Shortlisting
- Interview Scheduling & AI Candidate Matching
- Razorpay Payment Gateway, Subscriptions, Credits, Billing & Invoices

Phase 2 menu items are displayed disabled in the Recruiter Sidebar with clear "Coming in Phase 2" indicators to maintain UI alignment without fake functionality.

---

## 🛠 Technology Stack

### Backend
- **Framework**: Python 3.14 + FastAPI
- **Database**: PostgreSQL (with SQLite fallback for fast local test runs)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Auth & Security**: JWT (`python-jose`), Password Hashing (`passlib[bcrypt]`), Pydantic v2 schemas
- **Testing**: Pytest + FastAPI TestClient

### Frontend
- **Framework**: Vue 3 (Composition API `<script setup>`)
- **State Management**: Pinia
- **Routing**: Vue Router 4 (with Navigation Guards)
- **HTTP Client**: Axios (with Bearer Token Request/Response Interceptors)
- **Build Tool**: Vite 4
- **Design System**: CareerPilot AI Figma Design Language (Custom CSS variables, AppButton, AppCard, AppInput, AppSelect, AppBadge, AppModal, AppTable, AppToast, AppLoader, AppEmptyState)

---

## 📁 Repository Directory Structure

```
careerpilot-ai/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py           # Environment and app settings
│   │   │   ├── database.py         # SQLAlchemy engine & session setup
│   │   │   └── security.py         # Passlib hashing & JWT token management
│   │   ├── models/                 # Database models
│   │   │   ├── user.py             # User & UserRole enum
│   │   │   ├── company.py          # Company & VerificationStatus enum
│   │   │   ├── recruiter.py        # Recruiter profile link
│   │   │   └── job.py              # Job & JobSkill models
│   │   ├── schemas/                # Pydantic data schemas
│   │   │   ├── auth.py
│   │   │   ├── company.py
│   │   │   ├── recruiter.py
│   │   │   └── job.py
│   │   ├── repositories/           # Database access layer
│   │   │   ├── user_repository.py
│   │   │   ├── company_repository.py
│   │   │   ├── recruiter_repository.py
│   │   │   └── job_repository.py
│   │   ├── services/               # Business logic layer
│   │   │   ├── auth_service.py
│   │   │   ├── company_service.py
│   │   │   └── job_service.py
│   │   ├── dependencies/
│   │   │   └── auth.py             # JWT & Recruiter role dependency
│   │   ├── routers/                # REST API Endpoint routes
│   │   │   ├── auth.py
│   │   │   ├── company.py
│   │   │   ├── recruiter.py
│   │   │   └── jobs.py
│   │   └── main.py                 # FastAPI application entry point
│   ├── alembic/                    # Database migration scripts
│   ├── tests/                      # Pytest unit & integration test suite
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_company.py
│   │   ├── test_jobs.py
│   │   └── test_security_ownership.py
│   ├── requirements.txt            # Python dependencies
│   ├── seed.py                     # Demo data population script
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── styles/
│   │   │   ├── variables.css       # CareerPilot AI design tokens
│   │   │   ├── global.css
│   │   │   └── components.css
│   │   ├── components/
│   │   │   ├── common/             # Reusable UI components
│   │   │   │   ├── AppButton.vue
│   │   │   │   ├── AppCard.vue
│   │   │   │   ├── AppInput.vue
│   │   │   │   ├── AppSelect.vue
│   │   │   │   ├── AppBadge.vue
│   │   │   │   ├── AppModal.vue
│   │   │   │   ├── AppTable.vue
│   │   │   │   ├── AppToast.vue
│   │   │   │   ├── AppLoader.vue
│   │   │   │   └── AppEmptyState.vue
│   │   │   ├── layout/             # Layout components
│   │   │   │   ├── AppHeader.vue
│   │   │   │   ├── AppSidebar.vue
│   │   │   │   └── DashboardLayout.vue
│   │   │   └── recruiter/
│   │   │       ├── VerificationBanner.vue
│   │   │       └── JobCard.vue
│   │   ├── views/recruiter/        # Recruiter pages
│   │   │   ├── RecruiterLogin.vue
│   │   │   ├── RecruiterRegister.vue
│   │   │   ├── RecruiterDashboard.vue
│   │   │   ├── CompanyProfile.vue
│   │   │   ├── Jobs.vue
│   │   │   ├── CreateJob.vue
│   │   │   ├── EditJob.vue
│   │   │   └── JobDetails.vue
│   │   ├── stores/                 # Pinia stores (auth, recruiter, jobs)
│   │   ├── services/               # Axios API modules
│   │   ├── router/                 # Vue router configuration & guards
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .env.example
└── README.md
```

---

## 🚀 Quick Start Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies
python -m pip install -r requirements.txt

# Run seed script (Creates demo recruiter & verified company)
python seed.py

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```

- **Interactive API Documentation (Swagger)**: Visit `http://localhost:8000/docs`
- **ReDoc Documentation**: Visit `http://localhost:8000/redoc`

### 2. Demo Credentials

After running `python seed.py`, log in with:
- **Email**: `sensha@careerpilot.ai`
- **Password**: `Password123!`
- **Company**: `CareerPilot Technologies` [`VERIFIED`]

---

### 3. Running Backend Unit Tests

```bash
cd backend
pytest -v
```

---

### 4. Frontend Setup

```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```

- **Recruiter Web Portal**: Visit `http://localhost:5173/recruiter/login`

---

## 🎓 Recommended Git Commit Message

```bash
git add .
git commit -m "feat(recruiter): implement phase 1 recruiter foundation and job management"
```
