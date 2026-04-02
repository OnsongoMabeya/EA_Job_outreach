# Contributing to EA Job Outreach Automation

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, etc.)
- **Log files** if applicable (`pipeline.log`)
- **Screenshots** if relevant

**Example Bug Report:**

```markdown
**Title:** Scraper fails when RemoteOK returns empty results

**Description:** The scraper crashes instead of falling back to We Work Remotely when RemoteOK returns 0 jobs.

**Steps to Reproduce:**
1. Run `python main.py`
2. Wait for scraper to query RemoteOK
3. Observe crash when 0 results returned

**Expected:** Should fall back to WWR automatically
**Actual:** Script crashes with IndexError

**Environment:**
- OS: macOS 14.2
- Python: 3.11.5
- Error log: [attach pipeline.log]
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear use case** - Why is this enhancement needed?
- **Proposed solution** - How should it work?
- **Alternatives considered** - What other approaches did you think about?
- **Impact** - Who benefits from this enhancement?

**Example Enhancement:**

```markdown
**Title:** Add support for LinkedIn job scraping

**Use Case:** LinkedIn has many EA jobs not found on RemoteOK/WWR

**Proposed Solution:**
- Add `linkedin_scraper.py` module
- Use LinkedIn Jobs API or web scraping
- Integrate into existing pipeline

**Alternatives:**
- Manual LinkedIn searches (current workaround)
- Third-party job aggregators

**Impact:** Would increase job coverage by ~40%
```

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/EA_Job_outreach.git
cd EA_Job_outreach
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines:

```python
# Good
def scrape_jobs(source_url: str) -> list[dict]:
    """
    Scrape job postings from a given URL.
    
    Args:
        source_url: The URL to scrape jobs from
        
    Returns:
        List of job dictionaries
    """
    jobs = []
    # Implementation
    return jobs

# Bad
def scrapeJobs(url):
    jobs=[]
    return jobs
```

### Code Organization

- **One class per file** when possible
- **Clear function names** that describe what they do
- **Type hints** for function parameters and return values
- **Docstrings** for all public functions and classes
- **Comments** for complex logic only

### Error Handling

Always handle errors gracefully:

```python
# Good
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    logger.error(f"Failed to fetch {url}: {e}")
    return []

# Bad
response = requests.get(url)
data = response.json()  # Could crash
```

### Logging

Use appropriate log levels:

```python
logger.debug("Detailed information for debugging")
logger.info("General informational messages")
logger.warning("Warning messages for non-critical issues")
logger.error("Error messages for failures")
```

### Testing

While this project doesn't currently have automated tests, when adding new features:

1. **Test manually** with various inputs
2. **Check edge cases** (empty results, API failures, etc.)
3. **Verify logging** works correctly
4. **Test error handling** by simulating failures

## Submitting Changes

### 1. Commit Your Changes

Write clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "Add support for LinkedIn job scraping"
git commit -m "Fix: Handle empty results from RemoteOK API"
git commit -m "Improve: Reduce Groq API token usage by 30%"

# Bad commit messages
git commit -m "Update code"
git commit -m "Fix bug"
git commit -m "Changes"
```

**Commit Message Format:**

```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How did you test these changes?

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tested manually
```

### 4. Code Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

## Project-Specific Guidelines

### Adding New Job Sources

When adding a new job scraping source:

1. Create a new method in `scraper.py` or a separate module
2. Follow the existing pattern (return list of job dictionaries)
3. Add error handling and fallback logic
4. Update `config.py` with any new settings
5. Document the new source in README.md

**Required job dictionary format:**

```python
{
    "url": "https://...",           # Required
    "title": "Job Title",           # Required
    "company": "Company Name",      # Required
    "location": "Remote",           # Required
    "description": "Full text...",  # Required
    "tags": ["tag1", "tag2"]        # Optional
}
```

### Modifying LLM Prompts

When changing AI prompts:

1. Test with at least 10 different jobs
2. Verify message quality and tone
3. Check token usage doesn't increase significantly
4. Document the change in commit message
5. Consider making it configurable in `config.py`

### Updating Dependencies

When adding new dependencies:

1. Add to `requirements.txt` with version pinning
2. Test installation in fresh virtual environment
3. Document why the dependency is needed
4. Check for license compatibility

## Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Review the README.md and documentation
3. Open a new issue with the "question" label

## Recognition

Contributors will be recognized in the project README and release notes.

Thank you for contributing! 🎉
