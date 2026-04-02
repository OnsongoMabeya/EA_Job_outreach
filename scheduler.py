"""
Scheduler Module
Runs the job outreach pipeline on a scheduled basis
"""

import schedule
import time
import logging
import sys
from datetime import datetime
from main import run_pipeline, setup_logging
from config import SCHEDULE_TIME, LOG_FILE


logger = logging.getLogger(__name__)


def scheduled_job():
    """Wrapper function for scheduled pipeline execution"""
    logger.info("="*70)
    logger.info(f"SCHEDULED RUN TRIGGERED at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*70)
    
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"Scheduled pipeline run failed: {e}", exc_info=True)


def run_scheduler():
    """
    Run the scheduler that executes the pipeline daily
    """
    setup_logging()
    
    print(f"\n{'='*70}")
    print(f"  EA JOB OUTREACH AUTOMATION - SCHEDULER")
    print(f"{'='*70}")
    print(f"\n📅 Schedule: Daily at {SCHEDULE_TIME}")
    print(f"📝 Logs: {LOG_FILE}")
    print(f"\n⏰ Scheduler started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Waiting for next scheduled run...\n")
    print(f"   Press Ctrl+C to stop the scheduler\n")
    print(f"{'='*70}\n")
    
    logger.info(f"Scheduler started - Daily runs at {SCHEDULE_TIME}")
    
    # Schedule the job
    schedule.every().day.at(SCHEDULE_TIME).do(scheduled_job)
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*70}")
        print(f"  SCHEDULER STOPPED")
        print(f"{'='*70}")
        print(f"\n⏹️  Scheduler stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        logger.info("Scheduler stopped by user")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"Scheduler error: {e}", exc_info=True)
        print(f"\n❌ Scheduler error: {e}\n")
        sys.exit(1)


def main():
    """Main entry point for scheduler"""
    run_scheduler()


if __name__ == "__main__":
    main()
