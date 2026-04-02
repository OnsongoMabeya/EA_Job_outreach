"""
LLM Message Generator Module
Generates personalized outreach messages using Groq API
"""

import json
import logging
import time
from typing import List, Dict
from groq import Groq
from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_TEMPERATURE,
    GROQ_MAX_TOKENS,
    SYSTEM_PROMPT,
    PROMPT_TEMPLATE,
    APPLICANT_PROFILE,
    VALIDATED_JOBS_FILE,
    REQUEST_DELAY
)

logger = logging.getLogger(__name__)


class LLMGenerator:
    """Generates personalized outreach messages using Groq API"""
    
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=GROQ_API_KEY)
        logger.info(f"Initialized Groq model: {GROQ_MODEL}")
    
    def generate_message(self, job: Dict) -> str:
        """
        Generate a personalized outreach message for a single job
        Returns the generated message text
        """
        job_title = job.get('job_title', 'N/A')
        company_name = job.get('company_name', 'N/A')
        job_description = job.get('job_description', 'N/A')
        
        # Truncate description if too long (to avoid token limits)
        max_desc_length = 2000
        if len(job_description) > max_desc_length:
            job_description = job_description[:max_desc_length] + "..."
        
        # Format the prompt with job details
        user_prompt = PROMPT_TEMPLATE.format(
            job_title=job_title,
            company_name=company_name,
            job_description=job_description,
            applicant_profile=APPLICANT_PROFILE
        )
        
        try:
            logger.debug(f"Generating message for: {job_title} at {company_name}")
            
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS,
            )
            message = response.choices[0].message.content.strip()
            
            logger.info(f"✓ Generated message for: {job_title} at {company_name}")
            return message
            
        except Exception as e:
            logger.error(f"Error generating message for {job_title} at {company_name}: {e}")
            return self._get_fallback_message(job_title, company_name)
    
    def _get_fallback_message(self, job_title, company_name):
        fallback_message = f"""Dear Hiring Manager at {company_name},

I am writing to express my strong interest in the {job_title} position. With over 4 years of experience supporting C-suite executives and founders, I have developed a comprehensive skill set in calendar management, travel coordination, inbox management, and cross-functional communication.

I am particularly drawn to this opportunity at {company_name} and would welcome the chance to discuss how my background in remote executive support could contribute to your team's success.

I look forward to the opportunity to speak with you further.

Best regards"""
        
        logger.warning(f"Using fallback message for: {job_title} at {company_name}")
        return fallback_message
    
    def generate_all_messages(self, jobs: List[Dict]) -> List[Dict]:
        """
        Generate outreach messages for all validated jobs
        Adds 'outreach_message' field to each job dictionary
        """
        logger.info(f"Generating outreach messages for {len(jobs)} jobs...")
        
        jobs_with_messages = []
        
        for idx, job in enumerate(jobs, 1):
            logger.info(f"Processing job {idx}/{len(jobs)}...")
            
            message = self.generate_message(job)
            
            # Add message to job data
            job_with_message = job.copy()
            job_with_message['outreach_message'] = message
            jobs_with_messages.append(job_with_message)
            
            # Rate limiting - delay between API calls
            if idx < len(jobs):
                time.sleep(REQUEST_DELAY)
        
        logger.info(f"Successfully generated {len(jobs_with_messages)} outreach messages")
        return jobs_with_messages
    
    def load_from_file(self, filename: str = VALIDATED_JOBS_FILE) -> List[Dict]:
        """Load validated jobs from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
            logger.info(f"Loaded {len(jobs)} validated jobs from {filename}")
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
        """Save jobs with messages to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(jobs)} jobs with messages to {filename}")
        except Exception as e:
            logger.error(f"Error saving jobs to file: {e}")
            raise


def main():
    """Test function for LLM generator module"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    generator = LLMGenerator()
    jobs = generator.load_from_file()
    
    if jobs:
        jobs_with_messages = generator.generate_all_messages(jobs)
        generator.save_to_file(jobs_with_messages)
        
        print(f"\n{'='*60}")
        print(f"MESSAGE GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"Generated messages for {len(jobs_with_messages)} jobs")
        print(f"Saved to: {VALIDATED_JOBS_FILE}")
        print(f"{'='*60}\n")
        
        # Show sample message
        if jobs_with_messages:
            sample = jobs_with_messages[0]
            print(f"\nSample Message:")
            print(f"{'-'*60}")
            print(f"Job: {sample.get('job_title', 'N/A')}")
            print(f"Company: {sample.get('company_name', 'N/A')}")
            print(f"\nMessage:")
            print(sample.get('outreach_message', 'N/A'))
            print(f"{'-'*60}\n")
    else:
        print("No validated jobs found. Run scraper.py and validator.py first.")


if __name__ == "__main__":
    main()
