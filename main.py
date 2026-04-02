"""
Main Pipeline Runner
Orchestrates the complete EA Job Outreach automation pipeline
"""

import logging
import sys
from datetime import datetime
from scraper import JobScraper
from validator import JobValidator
from llm_generator import LLMGenerator
from sheets_uploader import SheetsUploader
from csv_exporter import CSVExporter

# Try to import Excel exporter (optional)
try:
    from excel_exporter import ExcelExporter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
from config import LOG_FILE, LOG_FORMAT, LOG_LEVEL


def setup_logging():
    """Configure logging to both file and console"""
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def print_banner(text: str):
    """Print a formatted banner"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def run_pipeline():
    """
    Execute the complete job outreach pipeline:
    1. Scrape jobs from RemoteOK (and WWR if needed)
    2. Validate jobs against criteria
    3. Generate personalized outreach messages
    4. Upload to Google Sheets
    """
    logger = logging.getLogger(__name__)
    
    print_banner("EA JOB OUTREACH AUTOMATION PIPELINE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    stats = {
        'scraped': 0,
        'validated': 0,
        'uploaded': 0,
        'skipped': 0
    }
    
    try:
        # STEP 1: Scrape Jobs
        print_banner("STEP 1/4: SCRAPING JOBS")
        logger.info("Starting job scraping...")
        
        scraper = JobScraper()
        raw_jobs = scraper.scrape_all()
        scraper.save_to_file(raw_jobs)
        
        stats['scraped'] = len(raw_jobs)
        
        if not raw_jobs:
            logger.warning("No jobs scraped. Pipeline stopped.")
            print("\n⚠️  No jobs found. Please try again later or check your internet connection.\n")
            return stats
        
        print(f"✓ Scraped {len(raw_jobs)} jobs\n")
        
        # STEP 2: Validate Jobs
        print_banner("STEP 2/4: VALIDATING JOBS")
        logger.info("Starting job validation...")
        
        validator = JobValidator()
        validated_jobs = validator.validate_all(raw_jobs)
        
        stats['validated'] = len(validated_jobs)
        
        if not validated_jobs:
            logger.warning("No jobs passed validation. Pipeline stopped.")
            print("\n⚠️  No jobs passed validation criteria.\n")
            validator.print_summary()
            return stats
        
        print(f"✓ {len(validated_jobs)} jobs passed validation\n")
        
        # STEP 3: Generate Outreach Messages
        print_banner("STEP 3/4: GENERATING OUTREACH MESSAGES")
        logger.info("Starting message generation...")
        
        generator = LLMGenerator()
        jobs_with_messages = generator.generate_all_messages(validated_jobs)
        generator.save_to_file(jobs_with_messages)
        
        print(f"✓ Generated {len(jobs_with_messages)} personalized messages\n")
        
        # Step 4: Upload to Google Sheets (with CSV fallback)
        print(f"\n{'='*70}")
        print(f"  STEP 4/4: UPLOADING TO GOOGLE SHEETS")
        print(f"{'='*70}\n")
        
        logger.info("Starting Google Sheets upload...")
        
        try:
            uploader = SheetsUploader()
            result = uploader.upload_jobs(jobs_with_messages)
            
            print(f"✓ Uploaded {result['uploaded']} jobs to Google Sheets")
            if result['skipped'] > 0:
                print(f"⊘ Skipped {result['skipped']} duplicate jobs")
            
            sheet_url = uploader.get_sheet_url()
            print(f"\n📊 Google Sheet URL: {sheet_url}")
            
            stats = {
                'scraped': len(raw_jobs),
                'validated': len(validated_jobs),
                'messages_generated': len(jobs_with_messages),
                'uploaded': result['uploaded'],
                'skipped': result['skipped'],
                'sheet_url': sheet_url
            }
        
        except Exception as sheets_error:
            logger.warning(f"Google Sheets upload failed: {sheets_error}")
            logger.info("Falling back to file export...")
            
            print(f"\n⚠️  Google Sheets upload failed (storage quota exceeded)")
            print(f"📄 Exporting to files instead...\n")
            
            # Export to CSV
            csv_exporter = CSVExporter()
            csv_result = csv_exporter.export_jobs(jobs_with_messages)
            
            print(f"✓ Exported {csv_result['exported']} jobs to CSV")
            print(f"📁 CSV File: {csv_result['file']}")
            
            # Also export to Excel if available (better text wrapping)
            excel_file = None
            if EXCEL_AVAILABLE:
                try:
                    excel_exporter = ExcelExporter()
                    excel_result = excel_exporter.export_jobs(jobs_with_messages)
                    excel_file = excel_result['file']
                    print(f"\n✓ Exported {excel_result['exported']} jobs to Excel (with text wrapping)")
                    print(f"📊 Excel File: {excel_file}")
                    print(f"\n💡 Tip: Open the Excel file for better text wrapping and formatting!")
                except Exception as e:
                    logger.warning(f"Excel export failed: {e}")
                    print(f"\n⚠️  Excel export failed (install openpyxl for Excel support)")
            
            print(f"\nℹ️  You can manually upload to Google Sheets:")
            print(f"   1. Go to https://sheets.google.com")
            print(f"   2. Click 'File > Import > Upload'")
            print(f"   3. Select the CSV or Excel file above")
            
            stats = {
                'scraped': len(raw_jobs),
                'validated': len(validated_jobs),
                'messages_generated': len(jobs_with_messages),
                'exported_to_csv': csv_result['exported'],
                'csv_file': csv_result['file'],
                'excel_file': excel_file,
                'uploaded': 0
            }
        
        logger.info("Pipeline completed successfully")
        
    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user")
        print("\n\n⚠️  Pipeline interrupted by user\n")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        print(f"\n\n❌ Pipeline failed with error: {e}\n")
        print(f"Check {LOG_FILE} for detailed error information.\n")
        sys.exit(1)
    
    return stats


def main():
    """Main entry point"""
    setup_logging()
    
    try:
        stats = run_pipeline()
        
        # Exit with appropriate code
        if stats['uploaded'] > 0:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # No jobs uploaded
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
