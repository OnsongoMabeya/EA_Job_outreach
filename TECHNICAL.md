# Technical Documentation

This document provides technical details about the EA Job Outreach Automation pipeline architecture, implementation, and design decisions.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [System Design](#system-design)
- [Module Details](#module-details)
- [Data Flow](#data-flow)
- [API Integration](#api-integration)
- [Error Handling Strategy](#error-handling-strategy)
- [Performance Considerations](#performance-considerations)
- [Design Decisions](#design-decisions)
- [Future Improvements](#future-improvements)

## Architecture Overview

The pipeline follows a **modular, sequential processing architecture** with clear separation of concerns:

```bash
┌─────────────────────────────────────────────────────────────┐
│                      Main Orchestrator                       │
│                        (main.py)                             │
└──────────────┬──────────────────────────────────────────────┘
               │
               ├──► Step 1: Scraping (scraper.py)
               │    ├─► RemoteOK API
               │    └─► We Work Remotely RSS (fallback)
               │
               ├──► Step 2: Validation (validator.py)
               │    ├─► Remote work check
               │    ├─► English requirement check
               │    └─► Role relevance check
               │
               ├──► Step 3: Message Generation (llm_generator.py)
               │    └─► Groq API (Llama 3.1 8B Instant)
               │
               └──► Step 4: Data Export
                    ├─► Google Sheets (sheets_uploader.py)
                    ├─► CSV Export (csv_exporter.py) [fallback]
                    └─► Excel Export (excel_exporter.py) [fallback]
```

### Design Pattern

**Pipeline Pattern** with **Strategy Pattern** for exporters:

- Each step is independent and can be tested separately
- Steps communicate through well-defined data structures
- Fallback strategies for API failures
- Logging at each step for observability

## System Design

### Core Components

1. **Orchestrator** (`main.py`)
   - Coordinates all pipeline steps
   - Handles high-level error recovery
   - Manages logging setup
   - Provides user feedback

2. **Scraper** (`scraper.py`)
   - Multi-source job scraping
   - Automatic fallback mechanism
   - Rate limiting compliance
   - Data normalization

3. **Validator** (`validator.py`)
   - Rule-based filtering
   - Configurable criteria
   - Detailed rejection logging
   - Performance optimization

4. **LLM Generator** (`llm_generator.py`)
   - AI-powered message generation
   - Automatic retry with exponential backoff
   - Fallback to template messages
   - Token usage optimization

5. **Exporters**
   - Google Sheets integration
   - CSV export with HTML cleaning
   - Excel export with formatting
   - Duplicate detection

6. **Scheduler** (`scheduler.py`)
   - Time-based automation
   - Graceful shutdown handling
   - Error recovery
   - Logging integration

### Configuration Management

All configuration centralized in `config.py`:

```python
# Environment variables (from .env)
GROQ_API_KEY
GOOGLE_SHEETS_CREDENTIALS_FILE
GOOGLE_SHEET_NAME

# Search criteria
REMOTE_KEYWORDS
ROLE_KEYWORDS
ENGLISH_KEYWORDS

# LLM settings
GROQ_MODEL
GROQ_TEMPERATURE
GROQ_MAX_TOKENS
SYSTEM_PROMPT
PROMPT_TEMPLATE

# Applicant profile
APPLICANT_PROFILE

# Scheduler settings
SCHEDULE_TIME
SCHEDULE_TIMEZONE

# File paths
RAW_JOBS_FILE
VALIDATED_JOBS_FILE
LOG_FILE

# Logging
LOG_LEVEL
LOG_FORMAT
```

## Module Details

### scraper.py

**Purpose:** Fetch job postings from multiple sources

**Key Functions:**

```python
class JobScraper:
    def scrape_all() -> list[dict]:
        """Main entry point - tries all sources"""
        
    def _scrape_remoteok() -> list[dict]:
        """Primary source: RemoteOK JSON API"""
        
    def _scrape_weworkremotely() -> list[dict]:
        """Fallback source: WWR RSS feed"""
        
    def _normalize_job(raw_job: dict) -> dict:
        """Convert to standard format"""
```

**Data Structure:**

```python
{
    "url": str,           # Job posting URL
    "title": str,         # Job title
    "company": str,       # Company name
    "location": str,      # Job location
    "description": str,   # Full job description
    "tags": list[str]     # Optional tags
}
```

**Error Handling:**

- Network timeouts: 10-second timeout with retry
- API failures: Automatic fallback to secondary source
- Malformed data: Skip individual jobs, continue processing
- Empty results: Log warning, return empty list

### validator.py

**Purpose:** Filter jobs based on configurable criteria

**Validation Rules:**

1. **Remote Work Check:**

   ```python
   def _is_remote(job: dict) -> bool:
       # Check title, description, location for remote keywords
       # Case-insensitive matching
   ```

2. **English Requirement Check:**

   ```python
   def _requires_english(job: dict) -> bool:
       # Check if English is required
       # OR no other languages mentioned
   ```

3. **Role Relevance Check:**

   ```python
   def _is_relevant_role(job: dict) -> bool:
       # Match against EA/Admin keywords
       # Fuzzy matching for variations
   ```

**Performance:**

- O(n) complexity for validation
- Early exit on first failed criterion
- Regex compilation cached
- ~0.1ms per job validation

### llm_generator.py

**Purpose:** Generate personalized outreach messages using AI

**Key Features:**

- **Groq API Integration:** Fast inference with Llama 3.1 8B
- **Automatic Retry:** Exponential backoff for rate limits
- **Fallback Messages:** Template-based when API fails
- **Token Optimization:** Efficient prompts to minimize usage

**Message Generation Flow:**

```python
def generate_message(job: dict) -> str:
    1. Format prompt with job details + applicant profile
    2. Call Groq API with retry logic
    3. If successful: return AI-generated message
    4. If failed: return fallback template message
    5. Log token usage and errors
```

**Retry Strategy:**

```python
max_retries = 3
backoff_factor = 2

for attempt in range(max_retries):
    try:
        return groq_api.call()
    except RateLimitError:
        wait_time = backoff_factor ** attempt
        time.sleep(wait_time)
```

### sheets_uploader.py

**Purpose:** Upload jobs to Google Sheets with duplicate detection

**Key Features:**

- **Automatic sheet creation** if doesn't exist
- **Duplicate detection** by URL
- **Batch updates** for efficiency
- **Fallback to CSV/Excel** on quota errors

**Upload Process:**

```python
def upload_jobs(jobs: list[dict]) -> dict:
    1. Authenticate with Google Sheets API
    2. Get or create spreadsheet
    3. Fetch existing URLs (duplicate check)
    4. Filter out duplicates
    5. Append new jobs
    6. Return summary (uploaded, skipped, URL)
```

**Duplicate Detection:**

```python
def _get_existing_urls() -> set[str]:
    # Fetch first column (URLs) from sheet
    # Return as set for O(1) lookup
    # Cache for performance
```

### csv_exporter.py & excel_exporter.py

**Purpose:** Export jobs to CSV/Excel when Google Sheets fails

**CSV Export:**

- HTML tag stripping for clean text
- Proper escaping for special characters
- Timestamp in filename
- UTF-8 encoding

**Excel Export:**

- Automatic text wrapping
- Bold headers
- Optimized column widths
- Better formatting for long messages

## Data Flow

### Complete Pipeline Flow

```bash
1. User runs: python main.py
   ↓
2. main.py initializes logging
   ↓
3. JobScraper.scrape_all()
   ├─► Try RemoteOK API
   ├─► If < 5 jobs, try WWR RSS
   └─► Return raw_jobs[]
   ↓
4. Save to raw_jobs.json
   ↓
5. JobValidator.validate_all(raw_jobs)
   ├─► For each job:
   │   ├─► Check remote work
   │   ├─► Check English requirement
   │   └─► Check role relevance
   └─► Return validated_jobs[]
   ↓
6. Save to validated_jobs.json
   ↓
7. LLMGenerator.generate_all_messages(validated_jobs)
   ├─► For each job:
   │   ├─► Format prompt
   │   ├─► Call Groq API
   │   └─► Add message to job dict
   └─► Return jobs_with_messages[]
   ↓
8. SheetsUploader.upload_jobs(jobs_with_messages)
   ├─► Try Google Sheets
   ├─► If quota exceeded:
   │   ├─► Export to CSV
   │   └─► Export to Excel
   └─► Return summary
   ↓
9. Display summary to user
   ↓
10. Log completion
```

### Data Transformations

**Scraping → Validation:**

```python
# Input: Raw API response
{
    "id": "12345",
    "position": "Executive Assistant",
    "company": "TechCorp",
    ...
}

# Output: Normalized job dict
{
    "url": "https://...",
    "title": "Executive Assistant",
    "company": "TechCorp",
    "location": "Remote",
    "description": "Full text..."
}
```

**Validation → Message Generation:**

```python
# Input: Validated job
{
    "url": "...",
    "title": "...",
    ...
}

# Output: Job with message
{
    "url": "...",
    "title": "...",
    "llm_message": "Dear Hiring Manager, ..."
}
```

## API Integration

### Groq API

**Endpoint:** `https://api.groq.com/openai/v1/chat/completions`

**Request Format:**

```python
{
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": formatted_prompt}
    ],
    "temperature": 0.7,
    "max_tokens": 300
}
```

**Rate Limits:**

- 14,400 requests/day (free tier)
- 30 requests/minute
- 100,000 tokens/day

**Error Codes:**

- `429`: Rate limit exceeded → Retry with backoff
- `400`: Bad request → Log and use fallback
- `401`: Invalid API key → Fail fast
- `500`: Server error → Retry

### Google Sheets API

**Authentication:** Service Account with JSON credentials

**Key Operations:**

```python
# Create spreadsheet
spreadsheet = gc.create(title)

# Get spreadsheet
spreadsheet = gc.open(title)

# Get all values
values = worksheet.get_all_values()

# Append rows
worksheet.append_rows(data)
```

**Rate Limits:**

- 300 requests/minute per project
- 100 requests/100 seconds per user

**Quota Management:**

- Batch operations when possible
- Cache spreadsheet references
- Handle quota errors gracefully

### RemoteOK API

**Endpoint:** `https://remoteok.com/api`

**Response Format:**

```json
[
    {
        "id": "...",
        "position": "...",
        "company": "...",
        "url": "...",
        "description": "...",
        "tags": [...]
    }
]
```

- No Authentication Required

**Best Practices:**

- Respect rate limits (no official limit, but be reasonable)
- Add delay between requests
- Handle empty responses
- Validate data structure

## Error Handling Strategy

### Levels of Error Handling

1. **Function Level:**

   ```python
   try:
       result = risky_operation()
   except SpecificError as e:
       logger.error(f"Operation failed: {e}")
       return fallback_value
   ```

2. **Module Level:**

   ```python
   try:
       jobs = scraper.scrape_all()
   except Exception as e:
       logger.error(f"Scraping failed: {e}", exc_info=True)
       jobs = []  # Continue with empty list
   ```

3. **Pipeline Level:**

   ```python
   try:
       run_pipeline()
   except CriticalError as e:
       logger.critical(f"Pipeline failed: {e}")
       sys.exit(1)
   ```

### Fallback Strategies

| Component  | Primary        | Fallback           |
|------------|----------------|--------------------|
| Job Source | RemoteOK       | We Work Remotely   |
| LLM        | Groq API       | Template message   |
| Export     | Google Sheets  | CSV + Excel        |
| Scheduler  | Python schedule| Cron/Task Scheduler|

## Performance Considerations

### Bottlenecks

1. **Network I/O:** API calls are the slowest part
2. **LLM Generation:** ~1-2 seconds per job
3. **Google Sheets:** Batch operations help

### Optimizations

1. **Efficient Model:** Using `llama-3.1-8b-instant` (fastest)
2. **Duplicate Detection:** O(1) lookup with sets
3. **Batch Updates:** Single Google Sheets append
4. **Caching:** Regex compilation, spreadsheet references
5. **Early Exit:** Stop validation on first failed criterion

### Scalability

**Current Limits:**

- ~100 jobs per run (limited by Groq free tier)
- ~200 runs per day (Groq quota)
- Single-threaded processing

**Potential Improvements:**

- Parallel LLM calls (with rate limit handling)
- Database instead of JSON files
- Distributed processing for multiple users
- Caching of generated messages

## Design Decisions

### Why Python?

- Rich ecosystem for web scraping
- Excellent API client libraries
- Easy to read and maintain
- Great for automation scripts

### Why Groq over OpenAI/Anthropic?

- **Free tier:** 14,400 requests/day vs 20-100/day
- **Speed:** Extremely fast inference
- **Quality:** Llama 3.1 is high quality
- **Simplicity:** OpenAI-compatible API

### Why Google Sheets over Database?

- **Accessibility:** Non-technical users can view/edit
- **Collaboration:** Easy sharing
- **No setup:** No database server needed
- **Familiar:** Everyone knows spreadsheets

### Why Sequential Processing?

- **Simplicity:** Easier to debug and maintain
- **Reliability:** No race conditions
- **Sufficient:** Current performance is acceptable
- **Error Handling:** Easier to track failures

## Future Improvements

### Short Term

1. **Add unit tests** for critical functions
2. **Implement caching** for LLM responses
3. **Add more job sources** (LinkedIn, Indeed)
4. **Improve duplicate detection** (fuzzy matching)
5. **Add email notifications** for new jobs

### Long Term

1. **Web dashboard** for configuration and monitoring
2. **Database backend** for better data management
3. **Parallel processing** for faster execution
4. **Machine learning** for better job matching
5. **Multi-user support** with separate credentials
6. **Analytics dashboard** for job market insights
7. **Integration with ATS** (Applicant Tracking Systems)

### Technical Debt

- Add comprehensive test suite
- Improve error messages
- Add type checking with mypy
- Refactor large functions
- Add API documentation
- Implement proper logging levels

## Development Guidelines

### Adding New Features

1. Update `config.py` for new settings
2. Add module with clear interface
3. Integrate into `main.py` pipeline
4. Update documentation
5. Test thoroughly
6. Add logging

### Debugging Tips

1. **Check logs:** `pipeline.log` has detailed info
2. **Use DEBUG level:** Set `LOG_LEVEL = "DEBUG"` in config
3. **Test individual modules:** Run scraper/validator separately
4. **Check API responses:** Log raw API data
5. **Verify credentials:** Test Google Sheets/Groq separately

---

For questions or clarifications, please open an issue on GitHub.
