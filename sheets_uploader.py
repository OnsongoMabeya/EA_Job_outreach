"""
Google Sheets Uploader Module
Uploads validated jobs with outreach messages to Google Sheets
"""

import json
import logging
from typing import List, Dict
import gspread
from google.oauth2.service_account import Credentials
from config import (
    GOOGLE_SHEETS_CREDENTIALS_FILE,
    GOOGLE_SHEET_NAME,
    SHEET_HEADERS,
    VALIDATED_JOBS_FILE,
    DESCRIPTION_TRUNCATE_LENGTH
)

logger = logging.getLogger(__name__)


class SheetsUploader:
    """Handles uploading job data to Google Sheets"""
    
    def __init__(self):
        self.client = None
        self.sheet = None
        self.worksheet = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            logger.info("Authenticating with Google Sheets API...")
            
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                GOOGLE_SHEETS_CREDENTIALS_FILE,
                scopes=scopes
            )
            
            self.client = gspread.authorize(creds)
            logger.info("✓ Successfully authenticated with Google Sheets API")
            
        except FileNotFoundError:
            logger.error(f"Credentials file not found: {GOOGLE_SHEETS_CREDENTIALS_FILE}")
            raise
        except Exception as e:
            logger.error(f"Error authenticating with Google Sheets: {e}")
            raise
    
    def _get_or_create_sheet(self):
        """Get existing sheet or create new one"""
        try:
            # Try to open existing sheet
            self.sheet = self.client.open(GOOGLE_SHEET_NAME)
            logger.info(f"Opened existing sheet: {GOOGLE_SHEET_NAME}")
            
        except gspread.SpreadsheetNotFound:
            # Create new sheet
            logger.info(f"Sheet not found. Creating new sheet: {GOOGLE_SHEET_NAME}")
            self.sheet = self.client.create(GOOGLE_SHEET_NAME)
            logger.info(f"✓ Created new sheet: {GOOGLE_SHEET_NAME}")
        
        # Get first worksheet
        self.worksheet = self.sheet.sheet1
        
        # Check if headers exist
        existing_headers = self.worksheet.row_values(1)
        
        if not existing_headers or existing_headers != SHEET_HEADERS:
            # Add headers
            self.worksheet.update('A1', [SHEET_HEADERS])
            logger.info("✓ Added header row to sheet")
    
    def _get_existing_urls(self) -> set:
        """Get set of URLs already in the sheet to avoid duplicates"""
        try:
            # Get all values from first column (URLs)
            url_column = self.worksheet.col_values(1)
            
            # Skip header row and return set of URLs
            existing_urls = set(url_column[1:]) if len(url_column) > 1 else set()
            
            logger.info(f"Found {len(existing_urls)} existing URLs in sheet")
            return existing_urls
            
        except Exception as e:
            logger.error(f"Error getting existing URLs: {e}")
            return set()
    
    def _truncate_description(self, description: str) -> str:
        """Truncate job description to specified length"""
        if len(description) <= DESCRIPTION_TRUNCATE_LENGTH:
            return description
        
        return description[:DESCRIPTION_TRUNCATE_LENGTH] + "..."
    
    def _prepare_row(self, job: Dict) -> List[str]:
        """Prepare a row of data for the sheet"""
        return [
            job.get('job_url', 'N/A'),
            job.get('job_title', 'N/A'),
            job.get('company_name', 'N/A'),
            job.get('location', 'N/A'),
            self._truncate_description(job.get('job_description', 'N/A')),
            job.get('outreach_message', 'N/A')
        ]
    
    def upload_jobs(self, jobs: List[Dict]) -> Dict[str, int]:
        """
        Upload jobs to Google Sheets
        Returns dict with counts of uploaded and skipped jobs
        """
        logger.info(f"Uploading {len(jobs)} jobs to Google Sheets...")
        
        # Get or create sheet
        self._get_or_create_sheet()
        
        # Get existing URLs to avoid duplicates
        existing_urls = self._get_existing_urls()
        
        # Prepare rows to upload
        rows_to_upload = []
        skipped_count = 0
        
        for job in jobs:
            job_url = job.get('job_url', '')
            
            if job_url in existing_urls:
                logger.debug(f"Skipping duplicate: {job.get('job_title', 'N/A')} at {job.get('company_name', 'N/A')}")
                skipped_count += 1
                continue
            
            row = self._prepare_row(job)
            rows_to_upload.append(row)
        
        # Upload new rows
        uploaded_count = 0
        if rows_to_upload:
            try:
                # Append all rows at once
                self.worksheet.append_rows(rows_to_upload, value_input_option='RAW')
                uploaded_count = len(rows_to_upload)
                logger.info(f"✓ Successfully uploaded {uploaded_count} new jobs")
                
            except Exception as e:
                logger.error(f"Error uploading rows to sheet: {e}")
                raise
        else:
            logger.info("No new jobs to upload (all were duplicates)")
        
        result = {
            'uploaded': uploaded_count,
            'skipped': skipped_count,
            'total': len(jobs)
        }
        
        return result
    
    def get_sheet_url(self) -> str:
        """Get the URL of the Google Sheet"""
        if self.sheet:
            return self.sheet.url
        return "N/A"
    
    def load_from_file(self, filename: str = VALIDATED_JOBS_FILE) -> List[Dict]:
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


def main():
    """Test function for sheets uploader module"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    uploader = SheetsUploader()
    jobs = uploader.load_from_file()
    
    if jobs:
        result = uploader.upload_jobs(jobs)
        
        print(f"\n{'='*60}")
        print(f"GOOGLE SHEETS UPLOAD COMPLETE")
        print(f"{'='*60}")
        print(f"✓ Uploaded: {result['uploaded']} jobs")
        print(f"⊘ Skipped (duplicates): {result['skipped']} jobs")
        print(f"Total processed: {result['total']} jobs")
        print(f"\nSheet URL: {uploader.get_sheet_url()}")
        print(f"{'='*60}\n")
    else:
        print("No jobs found. Run the full pipeline first.")


if __name__ == "__main__":
    main()
