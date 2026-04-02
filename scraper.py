"""
Job Scraper Module
Scrapes Executive Assistant job postings from RemoteOK and We Work Remotely
"""

import requests
import json
import time
import logging
import feedparser
from typing import List, Dict
from config import (
    REMOTEOK_API_URL,
    WEWORKREMOTELY_RSS_URL,
    MIN_JOBS_THRESHOLD,
    REQUEST_DELAY,
    RAW_JOBS_FILE,
    ROLE_KEYWORDS
)

logger = logging.getLogger(__name__)


class JobScraper:
    """Handles scraping jobs from multiple sources"""
    
    def __init__(self):
        self.jobs = []
    
    def scrape_remoteok(self) -> List[Dict]:
        """
        Scrape jobs from RemoteOK API
        Returns list of job dictionaries
        """
        logger.info("Scraping jobs from RemoteOK...")
        jobs = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(REMOTEOK_API_URL, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # RemoteOK API returns array where first element is metadata
            # Skip first element and process rest
            if isinstance(data, list) and len(data) > 1:
                for job in data[1:]:
                    # Filter for assistant-related roles
                    position = job.get('position', '').lower()
                    description = job.get('description', '').lower()
                    
                    # Check if job matches any role keywords
                    if any(keyword in position or keyword in description for keyword in ROLE_KEYWORDS):
                        job_data = {
                            'job_title': job.get('position', 'N/A'),
                            'company_name': job.get('company', 'N/A'),
                            'location': job.get('location', 'Remote'),
                            'job_description': job.get('description', 'N/A'),
                            'job_url': job.get('url', f"https://remoteok.com/remote-jobs/{job.get('id', '')}")
                        }
                        jobs.append(job_data)
                        logger.debug(f"Found job: {job_data['job_title']} at {job_data['company_name']}")
            
            logger.info(f"Scraped {len(jobs)} jobs from RemoteOK")
            
        except requests.RequestException as e:
            logger.error(f"Error scraping RemoteOK: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing RemoteOK JSON: {e}")
        except Exception as e:
            logger.error(f"Unexpected error scraping RemoteOK: {e}")
        
        return jobs
    
    def scrape_weworkremotely(self) -> List[Dict]:
        """
        Scrape jobs from We Work Remotely RSS feed
        Returns list of job dictionaries
        """
        logger.info("Scraping jobs from We Work Remotely (fallback)...")
        jobs = []
        
        try:
            feed = feedparser.parse(WEWORKREMOTELY_RSS_URL)
            
            for entry in feed.entries:
                # Extract job details from RSS entry
                title = entry.get('title', 'N/A')
                link = entry.get('link', 'N/A')
                description = entry.get('summary', 'N/A')
                
                # Try to parse company name from title (usually format: "Company: Job Title")
                company_name = 'N/A'
                job_title = title
                
                if ':' in title:
                    parts = title.split(':', 1)
                    company_name = parts[0].strip()
                    job_title = parts[1].strip()
                
                job_data = {
                    'job_title': job_title,
                    'company_name': company_name,
                    'location': 'Remote',
                    'job_description': description,
                    'job_url': link
                }
                jobs.append(job_data)
                logger.debug(f"Found job: {job_data['job_title']} at {job_data['company_name']}")
            
            logger.info(f"Scraped {len(jobs)} jobs from We Work Remotely")
            
        except Exception as e:
            logger.error(f"Error scraping We Work Remotely: {e}")
        
        return jobs
    
    def scrape_all(self) -> List[Dict]:
        """
        Scrape jobs from all sources
        Uses RemoteOK first, falls back to We Work Remotely if needed
        """
        logger.info("Starting job scraping process...")
        
        # Try RemoteOK first
        remoteok_jobs = self.scrape_remoteok()
        time.sleep(REQUEST_DELAY)
        
        all_jobs = remoteok_jobs
        
        # If RemoteOK yields fewer than threshold, use fallback
        if len(remoteok_jobs) < MIN_JOBS_THRESHOLD:
            logger.warning(f"RemoteOK returned only {len(remoteok_jobs)} jobs (threshold: {MIN_JOBS_THRESHOLD})")
            logger.info("Activating fallback: We Work Remotely")
            
            wwr_jobs = self.scrape_weworkremotely()
            all_jobs.extend(wwr_jobs)
            time.sleep(REQUEST_DELAY)
        
        # Remove duplicates based on URL
        unique_jobs = []
        seen_urls = set()
        
        for job in all_jobs:
            url = job.get('job_url')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_jobs.append(job)
        
        logger.info(f"Total unique jobs scraped: {len(unique_jobs)}")
        self.jobs = unique_jobs
        
        return unique_jobs
    
    def save_to_file(self, jobs: List[Dict], filename: str = RAW_JOBS_FILE):
        """Save scraped jobs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(jobs)} jobs to {filename}")
        except Exception as e:
            logger.error(f"Error saving jobs to file: {e}")
            raise


def main():
    """Test function for scraper module"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    scraper = JobScraper()
    jobs = scraper.scrape_all()
    scraper.save_to_file(jobs)
    
    print(f"\n{'='*60}")
    print(f"SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"Total jobs scraped: {len(jobs)}")
    print(f"Saved to: {RAW_JOBS_FILE}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
