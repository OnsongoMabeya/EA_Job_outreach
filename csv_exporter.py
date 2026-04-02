"""
CSV Exporter Module
Exports job data to CSV format as an alternative to Google Sheets
"""

import json
import csv
import logging
import re
from pathlib import Path
from datetime import datetime
from config import (
    VALIDATED_JOBS_FILE,
    SHEET_HEADERS
)

logger = logging.getLogger(__name__)


class CSVExporter:
    """Exports job data to CSV file"""
    
    def __init__(self, output_file=None):
        """
        Initialize CSV exporter
        
        Args:
            output_file: Path to output CSV file (default: ea_jobs_YYYYMMDD_HHMMSS.csv)
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"ea_jobs_{timestamp}.csv"
        
        self.output_file = Path(output_file)
        logger.info(f"Initialized CSV exporter: {self.output_file}")
    
    def load_from_file(self, filepath=VALIDATED_JOBS_FILE):
        """Load jobs from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
            logger.info(f"Loaded {len(jobs)} jobs from {filepath}")
            return jobs
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filepath}: {e}")
            return []
    
    def _clean_html(self, text):
        """Remove HTML tags and clean up text for CSV"""
        if not text or text == 'N/A':
            return text
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    def _prepare_row(self, job):
        """Prepare a single job row for CSV export"""
        # Get and clean description
        description = self._clean_html(job.get('job_description', 'N/A'))
        if len(description) > 500:
            description = description[:497] + "..."
        
        # Get and clean outreach message (preserve line breaks)
        outreach_message = job.get('outreach_message', 'N/A')
        
        return {
            'Job Posting URL': job.get('job_url', 'N/A'),
            'Job Title': job.get('job_title', 'N/A'),
            'Company Name': job.get('company_name', 'N/A'),
            'Location': job.get('location', 'Remote'),
            'Job Description': description,
            'LLM-Generated Outreach Message': outreach_message
        }
    
    def export_jobs(self, jobs):
        """
        Export jobs to CSV file
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            dict with export statistics
        """
        if not jobs:
            logger.warning("No jobs to export")
            return {
                'exported': 0,
                'total': 0,
                'file': str(self.output_file)
            }
        
        logger.info(f"Exporting {len(jobs)} jobs to CSV...")
        
        try:
            # Prepare rows
            rows = [self._prepare_row(job) for job in jobs]
            
            # Write to CSV
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=SHEET_HEADERS)
                writer.writeheader()
                writer.writerows(rows)
            
            logger.info(f"✓ Successfully exported {len(jobs)} jobs to {self.output_file}")
            
            return {
                'exported': len(jobs),
                'total': len(jobs),
                'file': str(self.output_file.absolute())
            }
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise
    
    def get_file_path(self):
        """Get the absolute path to the exported CSV file"""
        return str(self.output_file.absolute())


def main():
    """Test function for CSV exporter module"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    exporter = CSVExporter()
    jobs = exporter.load_from_file()
    
    if jobs:
        result = exporter.export_jobs(jobs)
        
        print(f"\n{'='*60}")
        print(f"CSV EXPORT COMPLETE")
        print(f"{'='*60}")
        print(f"✓ Exported: {result['exported']} jobs")
        print(f"Total processed: {result['total']} jobs")
        print(f"\nFile location: {result['file']}")
        print(f"\nYou can now:")
        print(f"  1. Open this CSV in Excel/Google Sheets")
        print(f"  2. Upload to Google Sheets manually")
        print(f"  3. Share with your team")
        print(f"{'='*60}\n")
    else:
        print("No jobs found. Run the full pipeline first.")


if __name__ == "__main__":
    main()
