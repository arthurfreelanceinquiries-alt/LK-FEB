# PORTAL LK-FEB — Technical Documentation
**Portal Manajemen Pengetahuan & Administrasi BEM FEB UKRIDA**

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Environment Variables](#environment-variables)
5. [Database Schema](#database-schema)
6. [Dependencies](#dependencies)
7. [Development Setup](#development-setup)
8. [Deployment](#deployment)
9. [Known Issues & Bug Tracking](#known-issues--bug-tracking)

---

## 1. Overview

Portal LK-FEB adalah sistem manajemen pengetahuan berbasis web yang dirancang untuk:
- **Centralized Knowledge Base**: Menyimpan semua dokumen proposal, SPU, LPU, dan arsip acara
- **Automated Document Management**: Generate, audit, dan arsip dokumen otomatis
- **Multi-Agent Collaboration**: Interface untuk koordinasi antar AI agents (lk-drafter, lk-auditor, lk-formatter, lk-orchestrator)
- **Real-time Dashboard**: Visualisasi status acara, timeline proyek, dan resource monitoring

**Current Status**: 🟡 Phase 0 - Initial MVP Build (Redesign in Progress)

---

## 2. Tech Stack

### Frontend
- **Framework**: TBD (Streamlit / React / Next.js - pending lk-formatter decision)
- **Styling**: TailwindCSS / Ant Design
- **State Management**: TBD (Context API / Zustand / Redux)

### Backend
- **Runtime**: Python 3.11+
- **Framework**: FastAPI / Flask (pending)
- **API Protocol**: REST / GraphQL (pending)
- **Authentication**: TBD (JWT / OAuth 2.0)

### Database
- **Primary DB**: Supabase (PostgreSQL 15+)
- **Storage**: Supabase Storage (for documents, PDFs, images)
- **Caching**: Redis (optional, future phase)

### Infrastructure
- **Hosting**: TBD (Vercel / Railway / AWS / DigitalOcean)
- **CI/CD**: GitHub Actions
- **Monitoring**: TBD (Sentry / LogRocket)

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PORTAL LK-FEB ARCHITECTURE                │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   Web Frontend   │◄─────►│   Backend API    │◄─────►│  Supabase DB     │
│   (UI Layer)     │       │   (FastAPI)      │       │  (PostgreSQL)    │
└──────────────────┘       └──────────────────┘       └──────────────────┘
         │                          │                           │
         │                          │                           │
         ▼                          ▼                           ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│  Hermes Agents   │       │  Python Scripts  │       │  Supabase        │
│  (lk-drafter,    │       │  (docx_generator,│       │  Storage         │
│   lk-auditor,    │       │   rab_validator, │       │  (Files)         │
│   lk-formatter)  │       │   typo_checker)  │       │                  │
└──────────────────┘       └──────────────────┘       └──────────────────┘

┌────────────────────────────────────────────────────────────┐
│                  DATA FLOW                                 │
│  User Request → Frontend → API → DB/Storage → Response    │
│  Agent Task → API → Execute Script → Store Result → Notify│
└────────────────────────────────────────────────────────────┘
```

**Design Principles**:
- **Single Source of Truth**: Supabase sebagai satu-satunya storage untuk semua data organisasi
- **API-First**: Semua operasi melalui REST API untuk memudahkan integrasi multi-client
- **Agent-Driven Automation**: AI agents trigger workflows via API endpoints
- **Version Control**: Git-based document versioning untuk proposal/SPU/LPU

---

## 4. Environment Variables

### Required Variables (Production)
```bash
# Database
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_KEY=[your-anon-key]
SUPABASE_SERVICE_KEY=[your-service-role-key]

# Authentication (if implemented)
JWT_SECRET_KEY=[random-secure-string]
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Storage
SUPABASE_BUCKET_NAME=bem-feb-documents

# Application
APP_ENV=production
APP_DEBUG=false
APP_PORT=8000
ALLOWED_ORIGINS=https://portal.bemfeb.ukrida.ac.id

# GitHub (for Git-based versioning)
GITHUB_TOKEN=[personal-access-token]
GITHUB_REPO=arthurfreelanceinquiries-alt/LK-FEB
```

### Development Variables
```bash
# Development overrides
APP_ENV=development
APP_DEBUG=true
APP_PORT=3000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Security Notes**:
- NEVER commit `.env` files to Git
- Use `.env.example` for template reference
- Rotate keys quarterly
- Use Supabase RLS (Row Level Security) policies

---

## 5. Database Schema

> **Status**: ⏳ Waiting for @lk-formatter to finalize Supabase setup
> 
> Schema akan di-generate berdasarkan mapping dari `bem_feb_data_master.xlsx`

### Proposed Tables Structure

#### 5.1 `events` (Acara)
```sql
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  nama_acara TEXT NOT NULL,
  tahun INTEGER NOT NULL,
  status TEXT CHECK (status IN ('triage', 'todo', 'ready', 'running', 'blocked', 'review', 'done', 'archived')),
  start_date DATE,
  due_date DATE,
  pic_name TEXT,
  pic_nim TEXT,
  proposal_file_url TEXT,
  spu_file_url TEXT,
  lpu_file_url TEXT,
  rab_json JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_tahun ON events(tahun);
```

#### 5.2 `documents` (Proposal, SPU, LPU)
```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  doc_type TEXT CHECK (doc_type IN ('proposal', 'spu', 'lpu', 'audit_review', 'surat', 'lpj')),
  file_name TEXT NOT NULL,
  file_url TEXT NOT NULL,
  markdown_content TEXT,
  version INTEGER DEFAULT 1,
  created_by TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_documents_event_id ON documents(event_id);
CREATE INDEX idx_documents_doc_type ON documents(doc_type);
```

#### 5.3 `members` (Kepengurusan BEM)
```sql
CREATE TABLE members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  nama_lengkap TEXT NOT NULL,
  nim TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  tanggal_lahir DATE,
  alamat TEXT,
  no_rekening TEXT,
  jurusan TEXT,
  tahun_masuk INTEGER,
  jabatan TEXT NOT NULL,
  divisi TEXT,
  foto_formal_url TEXT,
  foto_divisi_url TEXT,
  status TEXT CHECK (status IN ('active', 'inactive', 'alumni')) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_members_nim ON members(nim);
CREATE INDEX idx_members_jabatan ON members(jabatan);
```

#### 5.4 `timeline_tasks` (Timeline BEM)
```sql
CREATE TABLE timeline_tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  task_title TEXT NOT NULL,
  task_owner TEXT[],
  start_date DATE,
  due_date DATE,
  duration INTEGER,
  status TEXT CHECK (status IN ('Not Started', 'On progress', 'Completed', 'OFF TRACK')),
  jobs_component TEXT,
  file_reference TEXT,
  keterangan TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_timeline_status ON timeline_tasks(status);
CREATE INDEX idx_timeline_dates ON timeline_tasks(start_date, due_date);
```

#### 5.5 `finance` (Keuangan BEM)
```sql
CREATE TABLE finance (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  member_id UUID REFERENCES members(id),
  bulan TEXT NOT NULL,
  tahun INTEGER NOT NULL,
  status_bayar BOOLEAN DEFAULT FALSE,
  jumlah NUMERIC(15,2),
  keterangan TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_finance_member ON finance(member_id);
CREATE INDEX idx_finance_periode ON finance(bulan, tahun);
```

#### 5.6 `sponsors` (Target Sponsor & Media Partner)
```sql
CREATE TABLE sponsors (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  nama TEXT NOT NULL,
  kategori TEXT CHECK (kategori IN ('sponsor', 'media_partner')),
  telepon TEXT,
  email TEXT,
  tanggal_pendekatan DATE,
  status_respon TEXT,
  tanggal_followup DATE,
  keterangan TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sponsors_kategori ON sponsors(kategori);
CREATE INDEX idx_sponsors_status ON sponsors(status_respon);
```

#### 5.7 `audit_logs` (Audit Review History)
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  auditor TEXT NOT NULL,
  audit_type TEXT CHECK (audit_type IN ('struktur', 'isi', 'tipografi', 'rab')),
  score INTEGER CHECK (score >= 0 AND score <= 10),
  findings JSONB,
  status TEXT CHECK (status IN ('pass', 'fail', 'needs_revision')),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_document ON audit_logs(document_id);
CREATE INDEX idx_audit_logs_status ON audit_logs(status);
```

### Data Migration Strategy
1. **Phase 1**: Extract data dari `bem_feb_data_master.xlsx`
2. **Phase 2**: Transform ke format JSON sesuai schema
3. **Phase 3**: Load ke Supabase via Seed Script (`seed_database.py`)
4. **Phase 4**: Validate integrity & relationships

---

## 6. Dependencies

### Python Backend
```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
supabase==2.0.3
pydantic==2.5.0
python-dotenv==1.0.0
python-multipart==0.0.6
python-docx==1.1.0
openpyxl==3.1.2
pandas==2.1.3
jinja2==3.1.2

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
ruff==0.1.6
mypy==1.7.1
```

### Frontend (TBD - pending framework decision)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "next": "^14.0.0",
    "tailwindcss": "^3.3.0",
    "@supabase/supabase-js": "^2.38.0",
    "axios": "^1.6.0",
    "date-fns": "^2.30.0"
  }
}
```

---

## 7. Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (if using React/Next.js)
- Git
- Supabase CLI (optional, for local development)

### Initial Setup
```bash
# 1. Clone repository
git clone https://github.com/arthurfreelanceinquiries-alt/LK-FEB.git
cd LK-FEB

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your Supabase credentials

# 5. Run database migrations (after schema finalized)
python scripts/seed_database.py

# 6. Start development server
uvicorn main:app --reload --port 8000
```

### Running Tests
```bash
pytest tests/ -v --cov=app
```

---

## 8. Deployment

### Production Checklist
- [ ] Environment variables configured in hosting platform
- [ ] Database migrations applied to production Supabase
- [ ] Supabase RLS policies enabled
- [ ] CORS origins restricted to production domain
- [ ] SSL/TLS certificates configured
- [ ] Error monitoring (Sentry) active
- [ ] Backup strategy implemented
- [ ] CI/CD pipeline tested

### Deployment Platforms (Options)
1. **Vercel** (Recommended for Next.js frontend)
2. **Railway** (Full-stack Python + Node.js)
3. **DigitalOcean App Platform**
4. **AWS EC2 + RDS** (for full control)

---

## 9. Known Issues & Bug Tracking

> **Tracking File**: `00_SISTEM_BEM/PORTAL_BUG_TRACKING.md`

### Current Bugs (to be populated by @lk-drafter)
| ID | Severity | Component | Description | Status | Assigned To | Opened | Resolved |
|----|----------|-----------|-------------|--------|-------------|--------|----------|
| - | - | - | (akan diisi oleh @lk-drafter) | - | - | - | - |

### Bug Report Template
```markdown
## Bug ID: [AUTO_INCREMENT]
**Severity**: Critical / High / Medium / Low
**Component**: Frontend / Backend / Database / Scripts
**Reporter**: @agent-name
**Date Opened**: YYYY-MM-DD

### Description
(Deskripsi bug secara detail)

### Steps to Reproduce
1. Step 1
2. Step 2
3. Expected vs Actual

### Environment
- OS: Windows 11 / macOS / Linux
- Browser: Chrome 120 / Firefox / Safari
- Python Version: 3.11

### Proposed Fix
(Solusi yang disarankan)

### Status History
- [ ] Open
- [ ] In Progress (Assigned to: @agent-name)
- [ ] Fixed (Commit: #hash)
- [ ] Verified & Closed
```

---

## 📝 Changelog

> **Tracking File**: `00_SISTEM_BEM/PORTAL_CHANGELOG.md`

### Phase 0: Initial MVP Build (Current)
**Status**: 🟡 In Progress  
**Timeline**: Oct 2026 - Dec 2026  
**Goals**:
- [ ] Define tech stack & architecture
- [ ] Design database schema
- [ ] Create technical documentation
- [ ] Setup development environment

### Phase 1: UI/UX Redesign
**Status**: 🔴 Not Started  
**Timeline**: Jan 2027 - Feb 2027  
**Goals**:
- [ ] Design mockups (Figma)
- [ ] Implement responsive frontend
- [ ] User authentication flow
- [ ] Dashboard visualizations

### Phase 2: Supabase Migration
**Status**: 🔴 Not Started  
**Timeline**: Mar 2027 - Apr 2027  
**Goals**:
- [ ] Migrate Excel data to Supabase
- [ ] Implement API endpoints
- [ ] Setup Supabase Storage for files
- [ ] Configure RLS policies

### Phase 3: Production Deployment
**Status**: 🔴 Not Started  
**Timeline**: May 2027  
**Goals**:
- [ ] Deploy to production hosting
- [ ] Configure custom domain
- [ ] Setup monitoring & alerts
- [ ] User acceptance testing
- [ ] Official launch

---

## 📞 Support & Contact

**Technical Lead**: @lk-formatter (Database & Backend)  
**Project Manager**: @lk-orchestrator (Coordination)  
**Documentation**: @lk-arsiparis (Knowledge Base)

**GitHub Repository**: [arthurfreelanceinquiries-alt/LK-FEB](https://github.com/arthurfreelanceinquiries-alt/LK-FEB)

---

**Last Updated**: 14 Oktober 2026  
**Document Version**: 1.0.0  
**Maintained by**: @lk-arsiparis
