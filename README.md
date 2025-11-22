# WebDice - Automated Survey Filler

An intelligent automated survey filler for platforms like freecash.com and other survey websites. WebDice uses browser automation to detect and complete various survey types automatically.

## Features

- 🤖 **Automatic Survey Detection**: Detects survey platforms (Qualtrics, SurveyMonkey, TypeForm, Google Forms, etc.)
- 📝 **Multiple Question Types**: Handles radio buttons, checkboxes, text inputs, dropdowns, textareas, and number inputs
- 🎯 **Smart Response Generation**: Contextual responses based on question type and content
- ⚙️ **Configurable Behavior**: Customize selection strategies and response patterns
- 🔄 **Multi-page Support**: Automatically navigates through multi-page surveys
- 📸 **Screenshot Capability**: Capture survey completion for verification

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sushiomsky/webdice.git
cd webdice
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Quick Start

### Basic Usage

```python
from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig

# Create a configuration
config = SurveyConfig(
    selection_strategy='random',
    delay_between_questions=1.0,
    delay_between_pages=2.0
)

# Fill a survey
with SurveyFiller(config=config, headless=False) as filler:
    success = filler.fill_survey("https://example.com/survey")
    if success:
        print("Survey completed!")
        filler.take_screenshot("completed.png")
```

### Using Configuration File

```python
from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig

# Load config from YAML
config = SurveyConfig.from_yaml('config/default_config.yaml')

with SurveyFiller(config=config, headless=False) as filler:
    filler.fill_survey("https://example.com/survey")
```

### Run Example Scripts

```bash
# Basic usage example
python examples/basic_usage.py

# Using configuration file
python examples/with_config_file.py
```

## Configuration

Create a YAML configuration file to customize behavior:

```yaml
# Selection strategy: 'random', 'first', 'middle', 'last'
selection_strategy: random

# Delays (in seconds)
delay_between_questions: 1.0
delay_between_pages: 2.0

# Preferred responses for specific keywords
preferred_responses:
  satisfaction: high
  recommend: yes

# Demographics for profile questions
demographics:
  age: "25"
  country: "United States"
  employment: "Employed"
```

## Supported Question Types

- ✅ **Radio Buttons**: Single-choice questions
- ✅ **Checkboxes**: Multiple-choice questions
- ✅ **Text Inputs**: Short text responses with contextual generation
- ✅ **Textareas**: Long-form text responses
- ✅ **Dropdowns**: Select menus
- ✅ **Number Inputs**: Numeric responses with range validation

## Advanced Usage

### Headless Mode

Run surveys without visible browser window:

```python
with SurveyFiller(config=config, headless=True) as filler:
    filler.fill_survey(url)
```

### Custom Demographics

```python
config = SurveyConfig(
    demographics={
        'age': '30',
        'gender': 'male',
        'country': 'Canada',
        'employment': 'Self-employed'
    }
)
```

### Selection Strategies

- `random`: Randomly select from available options (default)
- `first`: Always select the first option
- `middle`: Select the middle option
- `last`: Always select the last option

## Supported Platforms

WebDice has been designed to work with:

- Qualtrics surveys
- SurveyMonkey
- TypeForm
- Google Forms
- Generic HTML forms
- Most standard survey platforms

## API Reference

### SurveyFiller

Main class for automated survey filling.

#### Methods

- `__init__(config, headless=False)`: Initialize the filler
- `fill_survey(url, max_pages=20)`: Complete a survey from start to finish
- `navigate_to_survey(url)`: Navigate to a survey URL
- `detect_survey_platform()`: Identify the survey platform
- `take_screenshot(filename)`: Capture current page screenshot

### SurveyConfig

Configuration class for survey behavior.

#### Parameters

- `selection_strategy`: Strategy for selecting options
- `delay_between_questions`: Delay in seconds between questions
- `delay_between_pages`: Delay in seconds between pages
- `preferred_responses`: Dictionary of preferred responses
- `demographics`: User demographic information

## Development

### Project Structure

```
webdice/
├── survey_filler/
│   ├── __init__.py
│   ├── survey_filler.py      # Main survey filler class
│   ├── question_handlers.py  # Question type handlers
│   └── config.py             # Configuration management
├── examples/
│   ├── basic_usage.py
│   └── with_config_file.py
├── config/
│   └── default_config.yaml
├── requirements.txt
├── setup.py
└── README.md
```

## Limitations

- Requires visible CAPTCHA to be solved manually
- Some surveys may have anti-bot protections
- Complex conditional logic in surveys may not be fully supported
- Rate limiting may apply on some platforms

## Ethical Considerations

This tool is designed for:
- Testing survey platforms
- Automating legitimate survey responses
- Personal use on platforms where automation is permitted

**Please ensure you:**
- Have permission to automate surveys
- Comply with platform terms of service
- Use responsibly and ethically

## Troubleshooting

### Browser not launching

Install Playwright browsers:
```bash
playwright install chromium
```

### Questions not being detected

- Check if the survey uses non-standard HTML elements
- Try adjusting delays in configuration
- Run in non-headless mode to debug visually

### Survey not completing

- Increase `max_pages` parameter
- Check logs for error messages
- Verify button selectors match the survey platform

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is provided for educational and testing purposes. Users are responsible for ensuring their use complies with applicable laws and terms of service.
