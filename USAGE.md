# Usage Guide - WebDice Automated Survey Filler

## Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/sushiomsky/webdice.git
cd webdice

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Basic Usage - Python API

```python
from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig

# Create configuration
config = SurveyConfig(
    selection_strategy='random',  # Options: 'random', 'first', 'middle', 'last'
    delay_between_questions=1.0,  # seconds
    delay_between_pages=2.0       # seconds
)

# Fill a survey
with SurveyFiller(config=config, headless=False) as filler:
    success = filler.fill_survey("https://example.com/survey")
    if success:
        print("Survey completed!")
```

### 3. Command Line Interface

```bash
# Basic usage
python survey_cli.py https://example.com/survey

# With custom configuration
python survey_cli.py https://example.com/survey -c config/my_config.yaml

# Run in headless mode (no visible browser)
python survey_cli.py https://example.com/survey --headless

# Save screenshot after completion
python survey_cli.py https://example.com/survey --screenshot result.png

# Verbose output for debugging
python survey_cli.py https://example.com/survey -v

# Limit number of pages
python survey_cli.py https://example.com/survey -m 5
```

## Configuration Options

### YAML Configuration File

Create a `config.yaml` file:

```yaml
# Selection strategy for multiple choice questions
# Options: random, first, middle, last
selection_strategy: random

# Time delays (in seconds)
delay_between_questions: 1.0
delay_between_pages: 2.0

# Preferred responses for specific keywords
preferred_responses:
  satisfaction: high
  recommend: yes
  frequency: often
  quality: excellent

# Demographics for profile-based questions
demographics:
  age: "25"
  gender: "prefer not to say"
  country: "United States"
  employment: "Employed"
  education: "Bachelor's degree"
  income: "50000-75000"
```

Load it in your code:

```python
from survey_filler.config import SurveyConfig

config = SurveyConfig.from_yaml('config.yaml')
```

### Programmatic Configuration

```python
from survey_filler.config import SurveyConfig

config = SurveyConfig(
    selection_strategy='random',
    delay_between_questions=0.5,
    delay_between_pages=1.5,
    demographics={
        'age': '30',
        'country': 'Canada',
        'employment': 'Self-employed'
    }
)
```

## Advanced Features

### 1. Running Multiple Surveys

```python
from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig

surveys = [
    "https://example.com/survey1",
    "https://example.com/survey2",
    "https://example.com/survey3"
]

config = SurveyConfig()

with SurveyFiller(config=config, headless=True) as filler:
    for i, survey_url in enumerate(surveys, 1):
        print(f"Filling survey {i}/{len(surveys)}")
        success = filler.fill_survey(survey_url)
        if success:
            filler.take_screenshot(f"survey_{i}_completed.png")
```

### 2. Custom Response Patterns

```python
# You can customize how the filler responds to different question types
# by modifying the configuration

config = SurveyConfig(
    selection_strategy='middle',  # Always select middle option
    delay_between_questions=2.0,  # Slower, more human-like
    demographics={
        'age': '35',
        'country': 'United Kingdom',
        'employment': 'Employed'
    }
)
```

### 3. Headless vs Visible Browser

```python
# Visible browser (good for debugging and testing)
with SurveyFiller(config=config, headless=False) as filler:
    filler.fill_survey(url)

# Headless browser (faster, good for automation)
with SurveyFiller(config=config, headless=True) as filler:
    filler.fill_survey(url)
```

### 4. Taking Screenshots

```python
with SurveyFiller(config=config, headless=False) as filler:
    filler.fill_survey(url)
    # Take screenshot at the end
    filler.take_screenshot("completed_survey.png")
```

## Supported Question Types

The survey filler can automatically detect and fill:

1. **Radio Buttons** - Single choice questions
2. **Checkboxes** - Multiple choice questions
3. **Text Inputs** - Short text responses
4. **Textareas** - Long-form text responses
5. **Dropdowns/Select** - Selection menus
6. **Number Inputs** - Numeric responses

### Context-Aware Text Generation

The filler intelligently generates responses based on the input field context:

- Email fields → `user1234@example.com`
- Name fields → `John Doe`, `Jane Smith`, etc.
- Age fields → Random age between 18-65
- Phone fields → `555-1234`
- City fields → Major city names
- Country fields → Country names
- Generic fields → Random appropriate responses

## Platform Support

WebDice works with surveys from:

- **Qualtrics** - Detected automatically
- **SurveyMonkey** - Detected automatically
- **TypeForm** - Detected automatically
- **Google Forms** - Detected automatically
- **Generic HTML Forms** - Works with standard HTML form elements

## Tips for Best Results

### 1. Start with Non-Headless Mode

When testing with a new survey, run in non-headless mode first to see what's happening:

```bash
python survey_cli.py https://example.com/survey
```

### 2. Adjust Delays for Different Platforms

Some platforms may need longer delays:

```yaml
delay_between_questions: 2.0
delay_between_pages: 3.0
```

### 3. Use Verbose Mode for Debugging

```bash
python survey_cli.py https://example.com/survey -v
```

### 4. Test with Sample Survey First

```bash
python examples/test_local_survey.py
```

This will open the local sample survey and demonstrate the filling process.

## Troubleshooting

### Problem: Browser doesn't open

**Solution:** Install Playwright browsers
```bash
playwright install chromium
```

### Problem: Questions not being detected

**Solution:** 
- Try increasing delays in configuration
- Run in non-headless mode to debug
- Check if survey uses non-standard HTML elements
- Use verbose mode: `-v`

### Problem: Survey doesn't complete

**Solution:**
- Increase `max_pages` parameter
- Check for CAPTCHA or anti-bot protections
- Verify the survey URL is correct
- Look at logs for error messages

### Problem: Import errors

**Solution:** Make sure you're in the correct directory
```bash
cd /path/to/webdice
python examples/basic_usage.py
```

## Examples

### Example 1: Simple Survey

```python
from survey_filler import SurveyFiller

with SurveyFiller(headless=False) as filler:
    filler.fill_survey("https://example.com/survey")
```

### Example 2: Batch Processing

```python
from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig
import time

config = SurveyConfig(selection_strategy='random')
survey_urls = [
    "https://example.com/survey1",
    "https://example.com/survey2",
    "https://example.com/survey3"
]

with SurveyFiller(config=config, headless=True) as filler:
    for url in survey_urls:
        print(f"Processing: {url}")
        filler.fill_survey(url)
        time.sleep(10)  # Wait between surveys
```

### Example 3: Custom Demographics

```python
from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig

config = SurveyConfig(
    demographics={
        'age': '28',
        'gender': 'female',
        'country': 'Australia',
        'employment': 'Self-employed',
        'education': 'Master\'s degree',
        'income': '75000-100000'
    }
)

with SurveyFiller(config=config) as filler:
    filler.fill_survey("https://example.com/survey")
```

## Ethical Guidelines

**Important:** Use this tool responsibly:

✅ **DO:**
- Use for testing your own surveys
- Use on platforms where automation is permitted
- Respect rate limits and platform guidelines
- Provide honest responses when appropriate

❌ **DON'T:**
- Violate terms of service
- Spam survey platforms
- Use for fraudulent purposes
- Abuse reward/compensation systems

## API Reference

### SurveyFiller Class

```python
SurveyFiller(config=None, headless=False)
```

**Methods:**
- `fill_survey(url, max_pages=20)` - Fill a complete survey
- `navigate_to_survey(url)` - Navigate to a survey URL
- `detect_survey_platform()` - Detect the survey platform type
- `take_screenshot(filename)` - Take a screenshot of current page

### SurveyConfig Class

```python
SurveyConfig(
    selection_strategy='random',
    delay_between_questions=1.0,
    delay_between_pages=2.0,
    preferred_responses={},
    demographics={}
)
```

**Methods:**
- `from_yaml(file_path)` - Load configuration from YAML file
- `to_yaml(file_path)` - Save configuration to YAML file

## Getting Help

If you encounter issues:

1. Check this usage guide
2. Review the README.md
3. Run with verbose flag: `-v`
4. Check the GitHub issues
5. Create a new issue with details about your problem

## Contributing

Contributions are welcome! Areas for improvement:
- Additional survey platform support
- More intelligent question detection
- Advanced answer strategies
- Better anti-bot detection handling
