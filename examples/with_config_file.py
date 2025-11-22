"""
Example using a configuration file
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig


def main():
    """
    Example: Fill out a survey using configuration from YAML file
    """
    
    # Load configuration from file
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'default_config.yaml')
    config = SurveyConfig.from_yaml(config_path)
    
    # Example survey URL (replace with actual survey URL)
    survey_url = "https://example.com/survey"
    
    print("Starting Survey Filler with config file...")
    print(f"Survey URL: {survey_url}")
    print(f"Strategy: {config.selection_strategy}")
    
    # Create and run survey filler
    with SurveyFiller(config=config, headless=False) as filler:
        success = filler.fill_survey(survey_url, max_pages=10)
        
        if success:
            print("✓ Survey completed successfully!")
        else:
            print("✗ Survey filling failed or incomplete")
    
    print("Done!")


if __name__ == "__main__":
    main()
