"""
Basic usage example of the Survey Filler
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig


def main():
    """
    Example: Fill out a survey using the automated survey filler
    """
    
    # Create configuration
    config = SurveyConfig(
        selection_strategy='random',
        delay_between_questions=1.0,
        delay_between_pages=2.0
    )
    
    # Example survey URL (replace with actual survey URL)
    survey_url = "https://example.com/survey"
    
    print("Starting Survey Filler...")
    print(f"Survey URL: {survey_url}")
    
    # Use context manager to handle browser lifecycle
    with SurveyFiller(config=config, headless=False) as filler:
        # Fill the survey
        success = filler.fill_survey(survey_url)
        
        if success:
            print("✓ Survey completed successfully!")
            # Take a final screenshot
            filler.take_screenshot("survey_completed.png")
        else:
            print("✗ Survey filling failed or incomplete")
    
    print("Done!")


if __name__ == "__main__":
    main()
