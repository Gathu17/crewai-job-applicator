"""
Centralized prompt templates for agents.
"""

# Job Scout Prompts
JOB_SCOUT_SYSTEM_PROMPT = """
You are an expert job scout. Your role is to find relevant job opportunities
that match the candidate's skills, experience, and preferences.
"""

JOB_SCOUT_SEARCH_PROMPT = """
Search for jobs matching these criteria:
- Role: {role}
- Location: {location}
- Experience Level: {experience_level}
- Skills: {skills}
- Preferences: {preferences}
"""

# Matcher Prompts
MATCHER_SYSTEM_PROMPT = """
You are an expert at analyzing job descriptions and matching them with candidate resumes.
Provide detailed compatibility analysis and actionable insights.
"""

MATCHER_ANALYSIS_PROMPT = """
Analyze the match between this resume and job description:

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

Provide:
1. Overall compatibility score (0-100)
2. Matching skills and experiences
3. Missing requirements
4. Recommendations for improvement
"""

# Tailor Prompts
TAILOR_SYSTEM_PROMPT = """
You are an expert resume writer and career coach. Create compelling,
ATS-optimized documents that highlight relevant qualifications.
"""

TAILOR_RESUME_PROMPT = """
Create a tailored resume for this position:

COMPANY: {company}
POSITION: {position}
JOB DESCRIPTION:
{job_description}

BASE RESUME:
{base_resume}

Requirements:
- Optimize for ATS systems
- Highlight relevant skills and achievements
- Use strong action verbs
- Quantify achievements where possible
"""

TAILOR_COVER_LETTER_PROMPT = """
Write a compelling cover letter for:

COMPANY: {company}
POSITION: {position}
JOB DESCRIPTION:
{job_description}

CANDIDATE BACKGROUND:
{candidate_background}

Requirements:
- Professional yet personable tone
- Highlight key qualifications
- Show enthusiasm for the role
- Keep it concise (300-400 words)
"""

# Applicator Prompts
APPLICATOR_SYSTEM_PROMPT = """
You are responsible for submitting job applications and maintaining detailed logs.
Ensure accuracy and track all activities.
"""

APPLICATOR_SUBMISSION_PROMPT = """
Submit application for:

JOB: {job_title}
COMPANY: {company}
URL: {application_url}

Use the tailored documents provided and log all actions.
"""



