# Testing Guide - Verify Your Setup

## Pre-Flight Checklist

Before testing, ensure:

- [ ] uv is installed: `uv --version`
- [ ] Node.js is installed: `node --version` (v18+)
- [ ] OpenAI API key is set in `.env`
- [ ] Backend dependencies installed: `uv sync`
- [ ] Frontend dependencies installed: `cd frontend && npm install`

## Test 1: Backend Health Check

### Start the Backend
```bash
uv run uvicorn main:app --reload
```

### Test the API
```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "llm_provider": "openai",
#   "monitoring": {...}
# }
```

### Visit API Docs
Open browser: http://localhost:8000/docs

You should see:
- Interactive Swagger UI
- All endpoints listed
- Try executing `/health` endpoint

✅ **Pass**: API responds with health data  
❌ **Fail**: See troubleshooting section below

## Test 2: Frontend Launch

### Start the Frontend
```bash
cd frontend
npm run dev
```

### Verify
Open browser: http://localhost:3000

You should see:
- Navigation bar with "JobBot AI" branding
- Dashboard page
- API Status indicator

✅ **Pass**: Frontend loads without errors  
❌ **Fail**: Check browser console for errors

## Test 3: Dashboard Integration

### On Dashboard Page
1. Check API Status - should show "Online" with green dot
2. Check Statistics cards - should show:
   - Total Calls: 0 (initially)
   - Success Rate: 0% or 100%
   - Total Tokens: 0
   - Total Cost: $0.0000

### Click "Refresh"
- Stats should reload
- No errors in browser console

✅ **Pass**: Dashboard shows data from backend  
❌ **Fail**: Check backend is running, check CORS settings

## Test 4: Process a Job (Full Workflow)

### Navigate to "Process Job" page

### Test Input
Use this sample data:

**Job Input:**
```
Senior Software Engineer
TechCorp Inc.

We are looking for an experienced Senior Software Engineer with:
- 5+ years of Python development
- Experience with FastAPI and Django
- React or Vue.js frontend experience
- AWS cloud infrastructure knowledge
- Strong problem-solving skills

Responsibilities:
- Design and build scalable APIs
- Mentor junior developers
- Collaborate with product team
- Write clean, maintainable code
```

**Base Resume:**
```
John Doe
Software Engineer
john@example.com | (555) 123-4567

EXPERIENCE
Software Engineer - Tech Solutions Inc (2020-2024)
- Built RESTful APIs using Python and FastAPI
- Developed frontend features with React
- Deployed applications on AWS EC2 and Lambda
- Mentored 3 junior developers

Junior Developer - StartupCo (2018-2020)
- Created web applications using Django
- Worked on Vue.js dashboard
- Implemented CI/CD pipelines

SKILLS
Python, JavaScript, FastAPI, Django, React, Vue.js, AWS, Docker, PostgreSQL

EDUCATION
BS Computer Science - University of Technology (2018)
```

### Click "Process Job Application"

### Expected Behavior
1. Button shows "Processing... (this may take 30-60 seconds)"
2. Loading state appears with animated spinner
3. Processing steps shown:
   - Analyzing job requirements...
   - Researching company information...
   - Tailoring your resume...
   - Generating final document...

### Expected Results (after 30-60 seconds)
✅ Success message appears
✅ Job Analysis section shows:
   - Role: "Senior Software Engineer"
   - Company: "TechCorp"
   - Required skills: Python, FastAPI, etc.
   - Key requirements listed

✅ Company Research section shows:
   - Industry information
   - Company culture
   - Interview tips

✅ Resume Tailoring section shows:
   - Skills highlighted
   - Key changes made
   - Recommendations

✅ Generated Resume section shows:
   - Formatted resume content
   - "Copy Resume" button works

### Test Copy Function
1. Click "Copy Resume" button
2. Button should show "✓ Copied!"
3. Paste into a text editor
4. Resume content should be there

✅ **Pass**: Full workflow completes with results  
❌ **Fail**: See error troubleshooting below

## Test 5: Monitoring Page

### Navigate to "Monitoring" page

### Expected Data
After running Test 4, you should see:
- Total LLM Calls: 5 (one per agent)
- Total Tokens: > 0
- Total Cost: > $0.0000
- Recent calls table with 5 rows

### Check Call Details
Each row should show:
- Timestamp
- Model (e.g., "gpt-4o-mini")
- Token count
- Cost
- Duration
- Success status (green badge)

### Test Reset
1. Click "Reset Stats" button
2. Confirm the dialog
3. All counters should reset to 0
4. Table should be empty

✅ **Pass**: Monitoring shows LLM usage data  
❌ **Fail**: Check if monitoring is enabled in backend

## Test 6: Error Handling

### Test Invalid Job Input
1. Go to Process Job page
2. Leave job input empty
3. Try to submit
4. Should show browser validation error

### Test API Error
1. Stop the backend server
2. Try to process a job
3. Should show connection error message
4. Start backend again
5. Should work normally

✅ **Pass**: Errors are handled gracefully  
❌ **Fail**: Check error handling in API service

## Troubleshooting

### Backend Won't Start

**Error: "No module named 'pydantic_settings'"**
```bash
uv sync
```

**Error: "Address already in use"**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows (then kill PID)
```

**Error: "OpenAI API key invalid"**
```bash
# Check .env file
cat .env | grep OPENAI_API_KEY

# Set environment variable directly
export OPENAI_API_KEY="your-key-here"  # Linux/Mac
$env:OPENAI_API_KEY="your-key-here"    # Windows PowerShell
```

### Frontend Won't Start

**Error: "Cannot find module"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 3000 already in use"**
```bash
# Update vite.config.ts to use different port
# Or kill process on port 3000
lsof -ti:3000 | xargs kill -9  # Mac/Linux
```

### API Connection Failed

**Error: "Network Error" in browser console**

1. Check backend is running: `curl http://localhost:8000/health`
2. Check CORS settings in `main.py`
3. Check `.env` has correct `VITE_API_URL`

### Slow LLM Response

**Takes more than 90 seconds**

1. Check your internet connection
2. Try a faster model: `LLM_MODEL=gpt-4o-mini` in `.env`
3. Check OpenAI API status: https://status.openai.com

### High Costs

**Unexpected high costs**

1. Check monitoring page for token usage
2. Use cheaper model: `gpt-4o-mini` instead of `gpt-4`
3. Reduce agent verbosity in config files
4. Check for infinite loops in logs

## Performance Benchmarks

### Expected Timings

| Operation | Expected Duration |
|-----------|------------------|
| Backend startup | 5-10 seconds |
| Frontend startup | 3-5 seconds |
| Health check API call | < 100ms |
| Full workflow execution | 30-60 seconds |
| Dashboard load | < 1 second |

### Expected Costs (using gpt-4o-mini)

| Operation | Approximate Cost |
|-----------|-----------------|
| Single workflow run | $0.01 - $0.05 |
| 10 workflow runs | $0.10 - $0.50 |
| 100 workflow runs | $1.00 - $5.00 |

*Note: Costs vary based on resume length and job description complexity*

## Success Criteria

All tests passing means:
- ✅ Backend API is healthy and responding
- ✅ Frontend loads and communicates with backend
- ✅ Full AI workflow executes successfully
- ✅ Results are displayed correctly
- ✅ Monitoring tracks LLM usage
- ✅ Error handling works properly

You're ready to use the system! 🎉
