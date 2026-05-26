# Quick Start - API Integration

## 🚀 Start the Application

### Terminal 1 - Backend
```bash
uv run uvicorn main:app --reload
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

## 📱 Access URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 Quick Test

### 1. Test API Health
Open browser: http://localhost:8000/health

Should return:
```json
{
  "status": "healthy",
  "llm_provider": "openai",
  "llm_model": "gpt-4o-mini"
}
```

### 2. Test Frontend
Open browser: http://localhost:5173

You should see:
- JobMatch header
- Navigation tabs
- Job Search page (default)

### 3. Test AI Workflow

Click **"AI Tailor"** tab, then use this sample data:

**Job Input**:
```
Senior Python Developer
RemoteTech Inc.

We're looking for an experienced Python developer with:
- 5+ years of Python development
- FastAPI and Django experience
- Frontend experience (React/Vue)
- AWS cloud deployment
- Strong problem-solving skills

Responsibilities:
- Build scalable REST APIs
- Develop new features
- Code reviews and mentoring
- DevOps and deployment
```

**Base Resume**:
```
John Smith
Software Engineer
john@example.com | 555-123-4567

EXPERIENCE
Senior Software Engineer - Tech Solutions (2020-2024)
• Built RESTful APIs with Python, FastAPI, and Django
• Developed React frontend components
• Deployed apps on AWS (EC2, Lambda, S3)
• Mentored 3 junior developers
• Improved API performance by 40%

Software Developer - StartupCo (2018-2020)
• Created web applications using Django and Vue.js
• Implemented CI/CD pipelines with GitHub Actions
• Worked on PostgreSQL database design

SKILLS
Python, JavaScript, FastAPI, Django, React, Vue.js, AWS, Docker, PostgreSQL, Redis, Git

EDUCATION
BS Computer Science - State University (2018)
```

**Company** (optional): `RemoteTech`

Click **"Generate Tailored Resume"** and wait 30-60 seconds.

### 4. Expected Results

After processing, you should see:

#### Job Analysis
- Role: Senior Python Developer
- Company: RemoteTech Inc.
- Required Skills: Python, FastAPI, Django, React/Vue, AWS
- Key Requirements: List of requirements

#### Company Research
- Industry information
- Company culture
- Interview tips

#### Resume Tailoring
- Skills Highlighted: Python, FastAPI, Django, etc.
- Key Changes Made: What was optimized
- Recommendations: Additional tips

#### Generated Resume
- Formatted, tailored resume
- Optimized for the job
- Copy button to copy to clipboard

### 5. Check Monitoring

Click **"Monitoring"** tab to see:
- **Total Calls**: Should show ~5 (one per agent)
- **Total Tokens**: Several thousand
- **Total Cost**: Around $0.01-$0.05
- **Success Rate**: 100%

#### Recent Calls Table
Shows 5 rows with:
- Timestamp
- Model (gpt-4o-mini or your configured model)
- Token counts
- Cost per call
- Duration (~5-15 seconds per call)
- Success status

## 🧪 API Endpoints Available

### Resume Crew (Main Workflow)
```bash
curl -X POST http://localhost:8000/jobs/resume-crew \
  -H "Content-Type: application/json" \
  -d '{
    "job_input": "job description here",
    "base_resume": "your resume here",
    "company_name": "optional company name"
  }'
```

### Monitoring - Get Stats
```bash
curl http://localhost:8000/monitoring/usage
```

### Monitoring - Get Summary
```bash
curl http://localhost:8000/monitoring/summary
```

### Monitoring - Reset
```bash
curl -X POST http://localhost:8000/monitoring/reset
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 🎨 UI Features

### AI Tailor Page
- Clean, modern interface
- Large text areas for easy input
- Real-time loading indicators
- Progress steps during processing
- Comprehensive results display
- One-click copy functionality

### Monitoring Page
- Statistics dashboard
- Real-time data
- Refresh button
- Reset functionality
- Detailed call history table

## ⚡ Tips

1. **First Run**: The first API call may take longer as models initialize
2. **Token Usage**: Longer resumes and job descriptions use more tokens
3. **Cost**: Using `gpt-4o-mini` is ~10x cheaper than `gpt-4`
4. **Caching**: Backend has result caching enabled by default
5. **Errors**: Check browser console and backend logs for details

## 🐛 Troubleshooting

### "Network Error" in browser
- Check backend is running: `curl http://localhost:8000/health`
- Check `.env` has correct `VITE_API_URL`
- Check CORS is enabled in backend

### "OpenAI API Error"
- Verify API key in `.env`
- Check OpenAI account has credits
- Try using `gpt-4o-mini` instead of `gpt-4`

### No data in Monitoring
- Run a workflow first to generate data
- Click Refresh button
- Check backend is running

### Slow Processing
- Normal: 30-60 seconds for full workflow
- Each of 5 agents makes an LLM call sequentially
- Faster model = faster results (gpt-4o-mini is fastest)

## 📊 Expected Performance

| Metric | Expected Value |
|--------|---------------|
| Processing Time | 30-60 seconds |
| LLM Calls per Workflow | 5 calls |
| Tokens per Workflow | 3,000-10,000 |
| Cost per Workflow (gpt-4o-mini) | $0.01-$0.05 |
| Success Rate | >95% |

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173 (or shown port)
- [ ] Health check returns "healthy"
- [ ] Can access API docs at /docs
- [ ] AI Tailor tab visible
- [ ] Can submit job and resume
- [ ] Results display after 30-60 seconds
- [ ] Can copy generated resume
- [ ] Monitoring shows statistics
- [ ] Call history visible in table

**Everything checked? You're ready to use the system! 🎉**
