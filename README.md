# Job Application Automation

AI-powered job application system using CrewAI agents and RAG technology to automatically discover, match, and tailor resumes for job opportunities.

##  Features

- **AI Resume Tailoring** - Automatically customize resumes for specific jobs
- **Job Discovery** - Search across LinkedIn, Jooble, and other job boards
- **Smart Matching** - RAG-powered job-resume compatibility scoring
- **LLM Monitoring** - Track AI usage, costs, and performance
- **RESTful API** - FastAPI backend with interactive docs
- **Modern UI** - React frontend with real-time updates

##  Quick Start

### 1. Install Dependencies

```bash
# Backend
uv sync

# Frontend
cd frontend && npm install
```

### 2. Configure Environment

Create `.env` file:
```env
OPENAI_API_KEY=your_key_here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
```

### 3. Start Services

```bash
# Backend (Terminal 1)
uv run uvicorn main:app --reload

# Frontend (Terminal 2)
cd frontend && npm run dev
```

### 4. Access Application

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

##  Usage

### AI Resume Tailor

1. Navigate to **AI Tailor** tab
2. Paste job description or URL
3. Paste your base resume
4. Click **Generate Tailored Resume**
5. Wait 30-60 seconds for AI processing
6. Copy your optimized resume

