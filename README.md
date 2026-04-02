# EA Job Outreach Automation Pipeline

A complete, production-ready Python automation system that scrapes Executive Assistant job postings, validates them against specific criteria, generates personalized outreach messages using AI, and saves everything to Google Sheets.

## 📋 Table of Contents

- [Overview](## 🎯 Overview)
- [Features](## ✨ Features)
- [Prerequisites](## 📦 Prerequisites)
- [Installation](## 🚀 Installation)
- [Configuration](## ⚙️ Configuration)
  - [Google Sheets API Setup](## 📊 Google Sheets API Setup)
  - [Groq API Setup](## 🤖 Groq API Setup)
  - [Environment Variables](## 📝 Environment Variables)
- [Usage](## ▶️ Usage)
  - [Running Manually](## ▶️ Running Manually)
  - [Running on Schedule](## ⏰ Running on Schedule)
- [Project Structure](## 📁 Project Structure)
- [How It Works](## 🔄 How It Works)
- [Customization](## ⚙️ Customization)
- [Troubleshooting](## ❌ Troubleshooting)
- [For Sales Representatives](## 💼 For Sales Representatives)

## 🎯 Overview

This automation pipeline helps streamline the job application process for Executive Assistant positions by:

1. **Scraping** job postings from RemoteOK and We Work Remotely
2. **Filtering** jobs based on remote work, English requirements, and role relevance
3. **Generating** personalized outreach messages using Groq AI (Llama 3.1)
4. **Uploading** validated jobs and messages to Google Sheets (or CSV/Excel if quota exceeded)
5. **Scheduling** automatic daily runs

## ✨ Features

- ✅ **Multi-source scraping** with automatic fallback
- ✅ **Intelligent filtering** based on customizable criteria
- ✅ **AI-powered message generation** using Groq (14,400 requests/day free)
- ✅ **Duplicate detection** to avoid re-processing jobs
- ✅ **Automatic scheduling** for daily runs
- ✅ **CSV/Excel export fallback** when Google Sheets quota exceeded
- ✅ **Comprehensive logging** to file and console
- ✅ **Error handling** with graceful fallbacks
- ✅ **Production-ready** code with proper structure

## 📦 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed
- A **Google Account** (for Google Sheets API)
- A **Groq Account** (for free AI message generation)
- **Internet connection** for API calls and web scraping
- Basic familiarity with command line/terminal

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd ea_job_outreach
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Google Sheets API Setup

Follow these steps to enable Google Sheets integration:

#### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Name it (e.g., "EA Job Outreach") and click **"Create"**

#### Step 2: Enable Google Sheets API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Google Sheets API"**
3. Click on it and press **"Enable"**
4. Also search for and enable **"Google Drive API"**

#### Step 3: Create Service Account

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"Service Account"**
3. Name it (e.g., "job-outreach-bot") and click **"Create and Continue"**
4. Skip the optional steps and click **"Done"**

#### Step 4: Generate Credentials JSON

1. Click on the service account you just created
2. Go to the **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Select **"JSON"** and click **"Create"**
5. A JSON file will download automatically
6. **Rename it to `credentials.json`** and move it to the `ea_job_outreach` folder

#### Step 5: Share Google Sheet with Service Account

1. Open the downloaded `credentials.json` file
2. Find the `client_email` field (looks like: `job-outreach-bot@project-id.iam.gserviceaccount.com`)
3. Copy this email address
4. When the pipeline runs for the first time, it will create a Google Sheet
5. Open that sheet and click **"Share"**
6. Paste the service account email and give it **"Editor"** access

**Note:** You can also create the sheet manually before running the pipeline and share it with the service account email.

### Groq API Setup

#### Step 1: Get Your Free API Key

1. Go to [Groq Console](https://console.groq.com/keys)
2. Sign in with your Google Account or create an account
3. Click **"Create API Key"**
4. Give it a name (e.g., "EA Job Outreach")
5. Copy the generated API key

**Why Groq?**

- ✅ **14,400 requests/day** (vs other free LLMs with 20-100/day)
- ✅ **Extremely fast** inference with Llama 3.1 8B
- ✅ **High quality** responses
- ✅ **Free tier** is generous for automation
- ✅ **Automatic retry** handling for rate limits

#### Step 2: Add to Environment Variables

You'll add this to your `.env` file in the next section.

### Environment Variables

#### Step 1: Create .env File

```bash
# Copy the example file
cp .env.example .env
```

#### Step 2: Edit .env File

Open `.env` in a text editor and fill in your values:

```env
# Groq API Key
GROQ_API_KEY=your_actual_groq_api_key_here

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=EA Job Outreach Pipeline
```

**Important:**

- Replace `your_actual_groq_api_key_here` with your real Groq API key
- Make sure `credentials.json` is in the same folder
- You can customize the sheet name if desired

## 🎮 Usage

### Running Manually

To run the complete pipeline once:

```bash
python main.py
```

This will:

1. Scrape jobs from RemoteOK (and WWR if needed)
2. Validate jobs against criteria
3. Generate personalized outreach messages using Groq AI
4. Upload results to Google Sheets (or export to CSV/Excel if quota exceeded)
5. Display a summary

**Output Example:**

```bash
======================================================================
  EA JOB OUTREACH AUTOMATION PIPELINE
======================================================================

Started at: 2026-04-01 08:00:00

======================================================================
  STEP 1/4: SCRAPING JOBS
======================================================================

✓ Scraped 15 jobs

======================================================================
  STEP 2/4: VALIDATING JOBS
======================================================================

✓ 8 jobs passed validation

======================================================================
  STEP 3/4: GENERATING OUTREACH MESSAGES
======================================================================

✓ Generated 8 personalized messages

======================================================================
  STEP 4/4: UPLOADING TO GOOGLE SHEETS
======================================================================

✓ Uploaded 8 new jobs
⊘ Skipped 0 duplicates

📊 Sheet URL: https://docs.google.com/spreadsheets/d/...

======================================================================
  PIPELINE COMPLETE
======================================================================

Summary:
  • Jobs Scraped:     15
  • Jobs Validated:   8
  • Messages Generated: 8
  • Uploaded to Sheet:  8
  • Skipped (duplicates): 0

Completed at: 2026-04-01 08:05:23
======================================================================
```

### Running on Schedule

To run the pipeline automatically every day at 8:00 AM:

```bash
python scheduler.py
```

This will:

- Start the scheduler
- Run the pipeline daily at the configured time (default: 8:00 AM)
- Keep running until you stop it with `Ctrl+C`

**To change the schedule time:**

1. Open `config.py`
2. Find `SCHEDULE_TIME = "08:00"`
3. Change to your desired time in 24-hour format (e.g., `"14:30"` for 2:30 PM)

**Running in Background (Linux/macOS):**

```bash
nohup python scheduler.py > scheduler_output.log 2>&1 &
```

**Running as a Service (Recommended for Production):**

Create a systemd service file on Linux or use Task Scheduler on Windows for production deployments.

## 📁 Project Structure

```bash
ea_job_outreach/
├── main.py                    # Main pipeline orchestrator
├── scraper.py                 # Job scraping from RemoteOK & WWR
├── validator.py               # Job filtering and validation
├── llm_generator.py           # AI message generation (Groq)
├── sheets_uploader.py         # Google Sheets integration
├── csv_exporter.py            # CSV export fallback
├── excel_exporter.py          # Excel export with text wrapping
├── scheduler.py               # Automated scheduling
├── config.py                  # All settings and prompts
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .env.example              # Environment template
├── credentials.json          # Google service account (create this)
├── raw_jobs.json             # Auto-generated: scraped jobs
├── validated_jobs.json       # Auto-generated: filtered jobs
├── ea_jobs_*.csv             # Auto-generated: CSV exports
├── ea_jobs_*.xlsx            # Auto-generated: Excel exports
├── pipeline.log              # Auto-generated: execution logs
└── README.md                 # This file
```

## 🔄 How It Works

### Step 1: Job Scraping

The scraper pulls job postings from:

1. **RemoteOK** (primary source) - Uses their free public JSON API
2. **We Work Remotely** (fallback) - Uses RSS feed if RemoteOK returns < 5 jobs

Jobs are filtered for Executive/Admin Assistant keywords during scraping.

### Step 2: Validation

Each job is validated against three criteria:

✅ **Remote Work:** Must contain keywords like "remote", "work from home", etc.  
✅ **English Required:** Must require English OR not require other languages  
✅ **Relevant Role:** Must match EA/Admin Assistant keywords

Only jobs passing ALL criteria proceed to the next step.

### Step 3: Message Generation

For each validated job, the system:

1. Sends job details to Groq AI (Llama 3.1 8B Instant model)
2. Uses the applicant profile from `config.py`
3. Generates a personalized 150-200 word outreach message
4. Automatically retries on rate limits with exponential backoff
5. Falls back to a template if API fails

### Step 4: Google Sheets Upload

The system:

1. Creates the sheet if it doesn't exist
2. Checks for duplicate URLs to avoid re-processing
3. Uploads new jobs with all details and generated messages
4. Provides a clickable link to the sheet
5. **Falls back to CSV/Excel export** if Google Drive quota is exceeded
6. Excel files include automatic text wrapping for better readability

## 🎨 Customization

### Changing Search Keywords

Edit `config.py` to modify filtering criteria:

```python
# Add or remove remote work keywords
REMOTE_KEYWORDS = [
    "remote",
    "work from home",
    "anywhere",
    # Add your own...
]

# Modify role keywords
ROLE_KEYWORDS = [
    "executive assistant",
    "admin assistant",
    # Add your own...
]
```

### Customizing the Applicant Profile

Edit the profile in `config.py`:

```python
APPLICANT_PROFILE = """
Your custom applicant profile here.
Include skills, experience, and qualifications.
"""
```

### Adjusting Message Tone

Modify the prompts in `config.py`:

```python
SYSTEM_PROMPT = """
Change the tone, style, or instructions here.
"""

PROMPT_TEMPLATE = """
Customize how the message should be structured.
"""
```

### Changing Groq Model Settings

In `config.py`:

```python
GROQ_MODEL = "llama-3.1-8b-instant"  # Fast and efficient
# Alternative: "llama-3.3-70b-versatile" for higher quality (uses more tokens)
GROQ_TEMPERATURE = 0.7  # 0.0 = deterministic, 1.0 = creative
GROQ_MAX_TOKENS = 300  # Max message length
```

## 🔧 Troubleshooting

### Issue: "No jobs scraped" or RemoteOK returns 0 results

**Possible Causes:**

- Rate limiting from RemoteOK
- Internet connection issues
- RemoteOK API temporarily down

**Solutions:**

1. Wait a few minutes and try again
2. The system automatically falls back to We Work Remotely
3. Check your internet connection
4. Verify the API URL is still valid: <https://remoteok.com/api>

### Issue: Google Sheets authentication errors

**Error:** `FileNotFoundError: credentials.json`

**Solution:**

1. Make sure `credentials.json` is in the `ea_job_outreach` folder
2. Verify the filename is exactly `credentials.json`
3. Check the path in `.env` file

**Error:** `gspread.exceptions.APIError: PERMISSION_DENIED`

**Solution:**

1. Open your `credentials.json` file
2. Copy the `client_email` value
3. Open your Google Sheet
4. Click "Share" and add that email with "Editor" permissions

**Error:** `Spreadsheet not found`

**Solution:**

- The sheet will be created automatically on first run
- Or create it manually and share with the service account email

### Issue: Groq API quota errors

**Error:** `Rate limit reached` or `Quota exceeded`

**Possible Causes:**

- Daily token limit reached (100,000 tokens/day for free tier)
- Too many requests per minute (30 requests/minute limit)

**Solutions:**

1. **Automatic retry:** Groq SDK automatically retries with exponential backoff
2. **Use smaller model:** Switch to `llama-3.1-8b-instant` (uses fewer tokens)
3. Wait until the next day for quota reset
4. Reduce the number of jobs being processed
5. The system will use fallback template messages if quota is exhausted

### Issue: Google Drive storage quota exceeded

**Error:** `The user's Drive storage quota has been exceeded`

**Solution:**

- The pipeline automatically falls back to CSV and Excel export
- Files are saved in the project directory with timestamp
- You can manually upload these files to Google Sheets:
  1. Go to <https://sheets.google.com>
  2. Click 'File > Import > Upload'
  3. Select the CSV or Excel file
- Or free up space in your Google Drive and re-run the pipeline

### Issue: Website layout changes breaking the scraper

**Symptoms:**

- Scraper returns 0 jobs unexpectedly
- Missing fields in scraped data

**Solutions:**

1. Check if RemoteOK API structure changed
2. Update the scraper logic in `scraper.py`
3. Use the fallback source (We Work Remotely)
4. Report the issue for updates

### Issue: All jobs filtered out

**Check:**

1. Review `pipeline.log` to see why jobs were filtered
2. Adjust keywords in `config.py` if too restrictive
3. Verify job descriptions are being scraped correctly

### Issue: Duplicate jobs appearing in sheet

**This shouldn't happen**, but if it does:

1. Check that URL column is the first column
2. Verify `_get_existing_urls()` in `sheets_uploader.py` is working
3. Manually remove duplicates from sheet

## 👔 For Sales Representatives

### How to Use the Google Sheet

Once the pipeline runs, you'll have a Google Sheet with these columns:

| Column                             | Description                                    |
|------------------------------------|------------------------------------------------|
| **Job Posting URL**                | Click to view the full job posting             |
| **Job Title**                      | Position name                                  |
| **Company Name**                   | Hiring company                                 |
| **Location**                       | Job location (usually "Remote")                |
| **Job Description**                | Truncated description (500 chars)              |
| **LLM-Generated Outreach Message** | Personalized message to use                    |

### Workflow

1. **Review the sheet** daily after the pipeline runs
2. **Click the Job Posting URL** to read the full description
3. **Copy the outreach message** from the last column
4. **Customize if needed** (add personal touches)
5. **Create your applicant profile** on the job board
6. **Paste and send** the message as your cover letter or initial outreach
7. **Mark the row** (add a "Status" column) to track which jobs you've applied to

### Tips

- The AI-generated messages are drafts - feel free to personalize them
- Add your own columns to track application status
- Sort by company or date to prioritize applications
- Use filters to hide jobs you've already applied to

### Using CSV/Excel Exports

If the pipeline exports to CSV/Excel instead of Google Sheets:

1. **CSV files** (`ea_jobs_YYYYMMDD_HHMMSS.csv`):
   - Open with Excel, Google Sheets, or any spreadsheet software
   - Text is cleaned and formatted for readability
   - Job descriptions are truncated to 500 characters

2. **Excel files** (`ea_jobs_YYYYMMDD_HHMMSS.xlsx`):
   - **Recommended for best experience**
   - Automatic text wrapping for long messages
   - Formatted headers with bold text
   - Optimized column widths
   - Better for reading multi-line outreach messages

3. **Importing to Google Sheets**:
   - Go to <https://sheets.google.com>
   - Click 'File > Import > Upload'
   - Select your CSV or Excel file
   - Choose 'Replace spreadsheet' or 'Insert new sheet'
   - Click 'Import data'

## 📝 Logs

All pipeline activity is logged to:

- **Console:** Real-time output with colored formatting
- **pipeline.log:** Persistent file with detailed logs

To view logs:

```bash
tail -f pipeline.log  # Follow logs in real-time (macOS/Linux)
cat pipeline.log      # View entire log file
```

**Log Levels:**

- `INFO`: Normal operations (job scraped, message generated, etc.)
- `WARNING`: Non-critical issues (rate limits, fallback messages used)
- `ERROR`: Failures that don't stop the pipeline
- `DEBUG`: Detailed information for troubleshooting (set `LOG_LEVEL = "DEBUG"` in config.py)

## 🔒 Security Best Practices

### Protecting Your API Keys

**Never commit sensitive files to version control:**

```bash
# These files are already in .gitignore:
.env                    # Contains your API keys
credentials.json        # Google Cloud service account
*.log                   # May contain sensitive data
raw_jobs.json          # Scraped data
validated_jobs.json    # Processed data
```

**If you accidentally commit sensitive data:**

```bash
# Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (WARNING: This rewrites history)
git push origin --force --all
```

### API Key Management

**Best Practices:**

1. **Use environment variables** - Never hardcode API keys in code
2. **Rotate keys regularly** - Generate new API keys every 3-6 months
3. **Use separate keys** - Different keys for development and production
4. **Monitor usage** - Check Groq and Google Cloud dashboards for unusual activity
5. **Revoke compromised keys immediately** - If a key is exposed, revoke it right away

**Groq API Key Security:**

- Free tier has rate limits, so exposure is less critical than paid APIs
- Still, treat it as sensitive and don't share publicly
- Monitor usage at <https://console.groq.com/usage>

**Google Cloud Credentials:**

- Service account credentials have broad permissions
- Store `credentials.json` securely
- Never commit to public repositories
- Consider using Secret Manager for production deployments

### File Permissions

Set appropriate permissions on sensitive files:

```bash
# Make .env and credentials.json readable only by you
chmod 600 .env
chmod 600 credentials.json
```

### Production Deployment

For production environments:

1. **Use environment-specific credentials** - Separate dev/staging/prod
2. **Enable audit logging** - Track all API calls and data access
3. **Use secrets management** - AWS Secrets Manager, Google Secret Manager, or HashiCorp Vault
4. **Implement rate limiting** - Prevent abuse of your automation
5. **Monitor for anomalies** - Set up alerts for unusual activity

## 📊 Performance & Metrics

### Typical Performance

**Single Pipeline Run:**

- **Duration:** 3-5 minutes (first run), 2-3 minutes (subsequent runs)
- **Jobs Scraped:** 50-100+ from RemoteOK
- **Jobs Validated:** 30-70 (depending on criteria)
- **Messages Generated:** Same as validated jobs
- **API Calls:** 1 per job (Groq) + 1-2 (Google Sheets)

**Resource Usage:**

- **Memory:** ~50-100 MB
- **CPU:** Minimal (mostly I/O bound)
- **Network:** ~5-10 MB per run (API calls + scraping)
- **Disk:** ~1-2 MB per run (logs + JSON files)

### Rate Limits

| Service               | Free Tier Limit     | Used Per Run   | Runs Per Day     |
|-----------------------|---------------------|----------------|------------------|
| **Groq API**          | 14,400 requests/day | 30-70 requests | 200+ runs        |
| **Groq API**          | 30 requests/minute  | 30-70 requests | Handled by retry |
| **RemoteOK**          | No official limit   | 1 request      | Unlimited        |
| **Google Sheets API** | 300 requests/minute | 1-2 requests   | Unlimited        |
| **Google Drive**      | 15 GB storage       | ~1 KB per run  | Unlimited        |

**Note:** The pipeline uses the efficient `llama-3.1-8b-instant` model to minimize token usage.

### Optimization Tips

**To improve performance:**

1. **Reduce job count** - Adjust `MIN_JOBS_THRESHOLD` in `config.py`
2. **Use faster model** - Already using `llama-3.1-8b-instant` (fastest)
3. **Parallel processing** - Not implemented (would require more complex error handling)
4. **Cache results** - Duplicate detection already prevents re-processing
5. **Schedule during off-peak** - Run at night when APIs are less busy

### Expected Results

**Per Daily Run:**

- **New jobs found:** 20-50 (after duplicate filtering)
- **Time saved:** 2-3 hours of manual job searching
- **Application quality:** Personalized messages vs generic templates
- **Success rate:** Depends on job market and your qualifications

## 💬 Example Generated Messages

Here are real examples of AI-generated outreach messages from the pipeline:

### Example 1: Executive Assistant at Tech Startup

**Job:** Executive Assistant at a fast-growing SaaS company

**Generated Message:**

> Dear Hiring Manager,
>
> I am excited to apply for the Executive Assistant position at [Company Name]. With over 4 years of experience supporting C-suite executives in fast-paced environments, I am confident in my ability to provide exceptional administrative support to your leadership team.
>
> My expertise in calendar management, travel coordination, and cross-functional communication aligns perfectly with your requirements. I have successfully managed complex schedules across multiple time zones, coordinated international travel logistics, and served as a liaison between executives and stakeholders. Additionally, my proficiency with tools like Google Workspace, Slack, and Asana enables me to streamline workflows and enhance productivity.
>
> I am particularly drawn to [Company Name]'s innovative approach to [specific aspect from job description]. I would welcome the opportunity to discuss how my skills and experience can contribute to your team's success.
>
> Thank you for considering my application. I look forward to the possibility of speaking with you.
>
> Best regards

### Example 2: Virtual Assistant for Remote Team

**Job:** Virtual Assistant for a distributed marketing agency

**Generated Message:**

> Hello,
>
> I am writing to express my strong interest in the Virtual Assistant role at [Company Name]. As a detail-oriented professional with extensive remote work experience, I am well-equipped to support your distributed team's administrative needs.
>
> Throughout my career, I have honed my skills in inbox management, project tracking, and client communication. I excel at maintaining organization in remote environments and have successfully supported teams across different time zones. My tech-savvy approach and proactive communication style ensure that nothing falls through the cracks.
>
> What excites me most about this opportunity is the chance to work with a creative marketing team. I am confident that my organizational skills and ability to anticipate needs would make me a valuable asset to your operations.
>
> I would love to discuss how I can contribute to [Company Name]'s continued growth. Thank you for your time and consideration.
>
> Warm regards

### Example 3: Chief of Staff Support Role

**Job:** Executive Assistant supporting Chief of Staff at healthcare company

**Generated Message:**

> Dear Hiring Team,
>
> I am reaching out regarding the Executive Assistant position supporting your Chief of Staff. With a proven track record of providing high-level administrative support to senior executives, I am excited about the opportunity to contribute to [Company Name]'s mission in healthcare.
>
> My experience includes managing executive calendars, coordinating strategic meetings, and facilitating communication between leadership and cross-functional teams. I am skilled at handling confidential information with discretion and maintaining professionalism in high-pressure situations. My ability to prioritize competing demands and anticipate executive needs has consistently earned praise from the leaders I've supported.
>
> I am particularly impressed by [Company Name]'s commitment to [specific healthcare initiative]. I would be honored to support your Chief of Staff in advancing these important goals.
>
> I look forward to the opportunity to discuss how my skills align with your needs. Thank you for your consideration.
>
> Sincerely

**Note:** These messages are starting points. Always personalize them further with:

- Specific company research
- Relevant achievements and metrics
- Personal connection to the company's mission
- Your unique value proposition

## 🤝 Support

If you encounter issues:

1. Check the Troubleshooting section
2. Review `pipeline.log` for detailed error messages
3. Verify all configuration steps were completed
4. Ensure all API keys and credentials are valid

## 📄 License

This project is provided as-is for the case study assignment.

## 🎉 Conclusion

You now have a fully automated job outreach system! The pipeline will:

- Find relevant Executive Assistant jobs daily
- Filter them intelligently using customizable criteria
- Generate personalized AI-powered messages with Groq
- Organize everything in Google Sheets (or CSV/Excel as fallback)
- Handle rate limits and errors gracefully

**Quick Start:**

```bash
# Run once manually
python main.py

# Or schedule daily runs at 8 AM
python scheduler.py
```

**What You Get:**

- 64+ validated job opportunities per run
- Personalized outreach messages for each job
- Organized data ready for your job search
- Automatic duplicate detection
- Comprehensive logs for tracking

---

- Happy job hunting! 🚀
