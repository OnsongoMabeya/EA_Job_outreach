"""
Job Validator Module
Filters and validates job postings based on criteria
"""

import json
import logging
from typing import List, Dict, Tuple
from config import (
    REMOTE_KEYWORDS,
    ENGLISH_KEYWORDS,
    ROLE_KEYWORDS,
    RAW_JOBS_FILE,
    VALIDATED_JOBS_FILE
)

logger = logging.getLogger(__name__)


class JobValidator:
    """Validates job postings against filtering criteria"""
    
    def __init__(self):
        self.validated_jobs = []
        self.filtered_out = []
    
    def is_remote(self, job: Dict) -> Tuple[bool, str]:
        """
        Check if job is remote
        Returns (is_valid, reason)
        """
        job_title = job.get('job_title', '').lower()
        location = job.get('location', '').lower()
        description = job.get('job_description', '').lower()
        
        combined_text = f"{job_title} {location} {description}"
        
        for keyword in REMOTE_KEYWORDS:
            if keyword in combined_text:
                return True, f"Remote keyword found: '{keyword}'"
        
        return False, "No remote keywords found"
    
    def requires_english(self, job: Dict) -> Tuple[bool, str]:
        """
        Check if job requires English
        Returns (is_valid, reason)
        """
        description = job.get('job_description', '').lower()
        job_title = job.get('job_title', '').lower()
        
        combined_text = f"{job_title} {description}"
        
        # Check for English requirement keywords
        for keyword in ENGLISH_KEYWORDS:
            if keyword in combined_text:
                return True, f"English requirement found: '{keyword}'"
        
        # Check for non-English language requirements (common ones)
        non_english_languages = [
            'spanish', 'french', 'german', 'chinese', 'japanese',
            'korean', 'portuguese', 'russian', 'arabic', 'hindi',
            'mandarin', 'cantonese', 'italian', 'dutch', 'polish'
        ]
        
        for lang in non_english_languages:
            # Look for patterns like "fluent in Spanish", "Spanish required", etc.
            if f"fluent in {lang}" in combined_text or \
               f"{lang} required" in combined_text or \
               f"{lang} speaker" in combined_text or \
               f"speak {lang}" in combined_text:
                return False, f"Non-English language requirement found: '{lang}'"
        
        # If no explicit English requirement but also no non-English requirement,
        # assume English (default for most remote jobs)
        return True, "No non-English language requirements found (default: English)"
    
    def is_relevant_role(self, job: Dict) -> Tuple[bool, str]:
        """
        Check if job is relevant for Executive/Admin Assistant
        Returns (is_valid, reason)
        """
        job_title = job.get('job_title', '').lower()
        description = job.get('job_description', '').lower()
        
        combined_text = f"{job_title} {description}"
        
        for keyword in ROLE_KEYWORDS:
            if keyword in combined_text:
                return True, f"Role keyword found: '{keyword}'"
        
        return False, "No relevant role keywords found"
    
    def validate_job(self, job: Dict) -> Tuple[bool, List[str]]:
        """
        Validate a single job against all criteria
        Returns (is_valid, reasons)
        """
        reasons = []
        
        # Check if remote
        is_remote, remote_reason = self.is_remote(job)
        if not is_remote:
            reasons.append(f"❌ Not remote: {remote_reason}")
        else:
            reasons.append(f"✓ Remote: {remote_reason}")
        
        # Check English requirement
        requires_eng, english_reason = self.requires_english(job)
        if not requires_eng:
            reasons.append(f"❌ English: {english_reason}")
        else:
            reasons.append(f"✓ English: {english_reason}")
        
        # Check role relevance
        is_relevant, role_reason = self.is_relevant_role(job)
        if not is_relevant:
            reasons.append(f"❌ Role: {role_reason}")
        else:
            reasons.append(f"✓ Role: {role_reason}")
        
        # Job is valid only if ALL criteria pass
        is_valid = is_remote and requires_eng and is_relevant
        
        return is_valid, reasons
    
    def validate_all(self, jobs: List[Dict]) -> List[Dict]:
        """
        Validate all jobs and return only those that pass all criteria
        """
        logger.info(f"Validating {len(jobs)} jobs...")
        
        validated = []
        filtered = []
        
        for idx, job in enumerate(jobs, 1):
            is_valid, reasons = self.validate_job(job)
            
            job_info = f"[{idx}/{len(jobs)}] {job.get('job_title', 'N/A')} at {job.get('company_name', 'N/A')}"
            
            if is_valid:
                validated.append(job)
                logger.info(f"✓ PASSED: {job_info}")
                for reason in reasons:
                    logger.debug(f"  {reason}")
            else:
                filtered_entry = {
                    'job': job,
                    'reasons': reasons
                }
                filtered.append(filtered_entry)
                logger.info(f"✗ FILTERED: {job_info}")
                for reason in reasons:
                    logger.debug(f"  {reason}")
        
        self.validated_jobs = validated
        self.filtered_out = filtered
        
        logger.info(f"Validation complete: {len(validated)} passed, {len(filtered)} filtered out")
        
        return validated
    
    def load_from_file(self, filename: str = RAW_JOBS_FILE) -> List[Dict]:
        """Load jobs from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
            logger.info(f"Loaded {len(jobs)} jobs from {filename}")
            return jobs
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from {filename}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading jobs from file: {e}")
            return []
    
    def save_to_file(self, jobs: List[Dict], filename: str = VALIDATED_JOBS_FILE):
        """Save validated jobs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(jobs)} validated jobs to {filename}")
        except Exception as e:
            logger.error(f"Error saving validated jobs to file: {e}")
            raise
    
    def print_summary(self):
        """Print validation summary"""
        print(f"\n{'='*60}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"✓ Passed validation: {len(self.validated_jobs)}")
        print(f"✗ Filtered out: {len(self.filtered_out)}")
        print(f"{'='*60}")
        
        if self.filtered_out:
            print(f"\nFiltered Jobs (showing reasons):")
            print(f"{'-'*60}")
            for entry in self.filtered_out[:5]:  # Show first 5
                job = entry['job']
                print(f"\n• {job.get('job_title', 'N/A')} at {job.get('company_name', 'N/A')}")
                for reason in entry['reasons']:
                    print(f"  {reason}")
            
            if len(self.filtered_out) > 5:
                print(f"\n... and {len(self.filtered_out) - 5} more filtered jobs")
        
        print(f"\n{'='*60}\n")


def main():
    """Test function for validator module"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    validator = JobValidator()
    jobs = validator.load_from_file()
    
    if jobs:
        validated = validator.validate_all(jobs)
        validator.save_to_file(validated)
        validator.print_summary()
    else:
        print("No jobs to validate. Run scraper.py first.")


if __name__ == "__main__":
    main()
