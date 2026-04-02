"""
Configuration file for EA Job Outreach Automation
Contains all settings, API configurations, and LLM prompts
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (loaded from environment variables)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "credentials.json")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "EA Job Outreach Pipeline")

# Job Search Keywords
REMOTE_KEYWORDS = [
    "remote",
    "work from home",
    "anywhere",
    "distributed",
    "telecommute",
    "wfh"
]

ENGLISH_KEYWORDS = [
    "english",
    "fluent",
    "native speaker",
    "proficient in english"
]

ROLE_KEYWORDS = [
    "executive assistant",
    "admin assistant",
    "administrative assistant",
    "ea",
    "va",
    "virtual assistant",
    "chief of staff support",
    "personal assistant",
    "office manager"
]

# Applicant Profile (used as context for LLM)
APPLICANT_PROFILE = """
A highly organized and proactive Executive/Virtual Assistant with 4+ years of experience 
supporting C-suite executives and founders. Skilled in calendar management, travel coordination, 
inbox management, project tracking, and cross-functional communication. Fluent in English, 
tech-savvy, detail-oriented, and experienced working remotely across time zones.
"""

# LLM Prompt Template
SYSTEM_PROMPT = """
You are a professional career coach helping an Executive Assistant craft personalized 
outreach messages for job applications. Your messages should be:
- Professional yet warm in tone
- Concise (150-200 words)
- Specific to the company and role
- Highlight relevant skills from the applicant's profile
- Include a clear call-to-action
"""

PROMPT_TEMPLATE = """
Write a personalized outreach message for the following job posting:

Job Title: {job_title}
Company Name: {company_name}
Job Description: {job_description}

Applicant Profile:
{applicant_profile}

Generate a professional, warm, and concise outreach message (150-200 words) that:
1. References the specific company and role
2. Highlights 2-3 relevant skills from the applicant's profile that match the job requirements
3. Expresses genuine interest in the position
4. Ends with a clear call-to-action

Do not include a subject line. Start directly with the greeting.
"""

# Scraper Settings
REMOTEOK_API_URL = "https://remoteok.com/api"
WEWORKREMOTELY_RSS_URL = "https://weworkremotely.com/categories/remote-administrative-jobs.rss"

# Minimum jobs threshold before using fallback
MIN_JOBS_THRESHOLD = 5

# Scheduler Settings
SCHEDULE_TIME = "08:00"  # 24-hour format (HH:MM)
SCHEDULE_TIMEZONE = "UTC"  # Change to your timezone if needed

# File Paths
RAW_JOBS_FILE = "raw_jobs.json"
VALIDATED_JOBS_FILE = "validated_jobs.json"
LOG_FILE = "pipeline.log"

# Google Sheets Column Headers
SHEET_HEADERS = [
    "Job Posting URL",
    "Job Title",
    "Company Name",
    "Location",
    "Job Description",
    "LLM-Generated Outreach Message"
]

# Logging Configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# Job Description Truncation Length (for Google Sheets)
DESCRIPTION_TRUNCATE_LENGTH = 500

# Groq Model Configuration
# Using 8b model - faster, uses fewer tokens, still high quality
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_TEMPERATURE = 0.7
GROQ_MAX_TOKENS = 300

# Rate Limiting (seconds between requests)
REQUEST_DELAY = 1
