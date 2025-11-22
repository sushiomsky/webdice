"""
Test the survey filler with a local HTML survey file
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig


def main():
    """
    Test survey filler with local sample survey
    """
    
    # Get path to sample survey
    project_root = Path(__file__).parent.parent
    survey_file = project_root / 'tests' / 'sample_survey.html'
    
    if not survey_file.exists():
        print(f"Error: Sample survey not found at {survey_file}")
        return 1
    
    # Convert to file URL
    survey_url = f"file://{survey_file.absolute()}"
    
    print("🧪 Testing Survey Filler with local sample survey")
    print(f"📄 Survey file: {survey_file}")
    print(f"🔗 URL: {survey_url}")
    print()
    
    # Create configuration
    config = SurveyConfig(
        selection_strategy='random',
        delay_between_questions=0.5,
        delay_between_pages=1.0
    )
    
    # Run survey filler
    print("🚀 Starting browser...")
    with SurveyFiller(config=config, headless=False) as filler:
        print("📝 Filling survey...")
        success = filler.fill_survey(survey_url, max_pages=1)
        
        if success:
            print()
            print("✅ Survey filled successfully!")
            
            # Take screenshot
            screenshot_path = project_root / 'test_survey_result.png'
            filler.take_screenshot(str(screenshot_path))
            print(f"📸 Screenshot saved: {screenshot_path}")
        else:
            print()
            print("❌ Failed to fill survey")
            return 1
    
    print()
    print("✨ Test completed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
