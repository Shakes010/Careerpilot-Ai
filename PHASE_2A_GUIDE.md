# CareerPilot AI — Phase 2A Guide

Welcome Sensha! This guide provides simple, beginner-friendly instructions for running and testing **Phase 2A (Project Collaboration & Career Sandbox)**.

---

## 📌 Phase 2A Features Overview

1. **Feature 31: Create / Join Project** (`/student/projects`, `/student/projects/create`, `/student/projects/:id`)
   - Create public or private collaboration projects with title, description, category, technology stack, and maximum team members.
   - Request to join public projects with join request tracking.
2. **Feature 32: Team Formation + Task Assignment** (`/student/projects/:id`)
   - View team members and assign specialized roles (`OWNER`, `MEMBER`, `TEAM_LEAD`, `FRONTEND`, `BACKEND`, `UI_UX`, `TESTING`).
   - Process join requests (Accept / Reject) with strict backend team capacity enforcement.
   - Create, assign, and update tasks (`TODO` → `IN_PROGRESS` → `COMPLETED`).
3. **Feature 33: Project Progress Tracking** (`/student/projects/:id`)
   - Dynamic progress percentage calculation formula: `completed_tasks / total_tasks * 100`.
   - Visual progress bar styled according to Figma CareerPilot AI guidelines.
4. **Feature 34: Project Completion Verification** (`/student/projects/:id`)
   - Submit completed project for verification review (`VERIFICATION_PENDING`).
   - Prevents self-approval; maintains state ready for Admin verification in Phase 2B.
5. **Feature 35: Career Sandbox** (`/student/career-sandbox`, `/student/career-sandbox/:id`, `/student/career-sandbox/attempt/:id`)
   - Browse published practice challenges by difficulty (`BEGINNER`, `INTERMEDIATE`, `ADVANCED`).
   - Start challenge attempts, view instructions, write code solutions, and submit for assessment system evaluation.

---

## 🚀 How to Run the Project (Beginner Instructions)

### Step 1: Database Seed
Populate demo student, project, and sandbox challenge data.

- **WHERE**: VS Code Terminal
- **COMMAND**:
  ```powershell
  cd D:\careerpilot-ai\backend
  python seed.py
  ```
- **WHAT IT DOES**: Drops and creates fresh database tables with initial test records.
- **EXPECTED RESULT**: Displays `Database Seed Completed Successfully!` with demo login credentials.

---

### Step 2: Start Backend Server
- **WHERE**: VS Code Terminal (Terminal Window 1)
- **COMMAND**:
  ```powershell
  cd D:\careerpilot-ai
  python run_backend.py
  ```
- **WHAT IT DOES**: Launches the FastAPI REST API server at `http://localhost:8000`.
- **EXPECTED RESULT**: Displays `Uvicorn running on http://127.0.0.1:8000`. You can open `http://localhost:8000/docs` in your browser to view interactive API documentation.

---

### Step 3: Start Frontend Server
- **WHERE**: VS Code Terminal (Terminal Window 2)
- **COMMAND**:
  ```powershell
  cd D:\careerpilot-ai\frontend
  npm run dev
  ```
- **WHAT IT DOES**: Starts Vite development server for the Vue 3 application.
- **EXPECTED RESULT**: Displays `Local: http://localhost:5173/`. Open it in your web browser.

---

### Step 4: Run Automated Test Suite
- **WHERE**: VS Code Terminal
- **COMMAND**:
  ```powershell
  cd D:\careerpilot-ai\backend
  pytest -v
  ```
- **WHAT IT DOES**: Executes all 19 automated unit & security tests across Auth, Jobs, Admin, Projects, and Sandbox.
- **EXPECTED RESULT**: Displays `19 passed in 10.33s` (100% PASS).

---

## 🔐 Credentials Summary

| Role | Email | Password |
|---|---|---|
| **Student** | `student@careerpilot.ai` | `Password123!` |
| **Recruiter** | `sensha@careerpilot.ai` | `Password123!` |
| **Admin** | `admin@careerpilot.ai` | `AdminPass123!` |
