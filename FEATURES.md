# WebDice Features

## Overview
WebDice is a comprehensive automated survey filler designed to work with platforms like freecash.com and other survey websites. It uses browser automation to intelligently detect and complete various types of survey questions.

## Core Capabilities

### 1. Multi-Platform Survey Support
- **Qualtrics**: Automatically detected and handled
- **SurveyMonkey**: Automatically detected and handled
- **TypeForm**: Automatically detected and handled
- **Google Forms**: Automatically detected and handled
- **Generic HTML Forms**: Works with standard HTML form elements
- **Auto-detection**: Platform is automatically identified by URL patterns

### 2. Question Type Handlers

#### Radio Buttons (Single Choice)
- Detects radio button groups by name attribute
- Supports multiple selection strategies:
  - `random`: Randomly selects an option (default)
  - `first`: Always selects the first option
  - `middle`: Selects the middle option
  - `last`: Always selects the last option
- Only selects visible and enabled options

#### Checkboxes (Multiple Choice)
- Independent checkbox handling
- Configurable check probability (default: 50%)
- Respects existing checked state
- Can check or uncheck based on strategy

#### Text Inputs
- Context-aware response generation
- Detects field type from name/placeholder:
  - Email fields → `user####@example.com`
  - Name fields → Realistic names from a pool
  - Age fields → Random age 18-65
  - Phone fields → `555-####` format
  - City fields → Major city names
  - Country fields → Country names
  - ZIP/Postal codes → Numeric codes
  - Generic fields → Appropriate generic responses

#### Textareas (Long-form Text)
- Multi-line text responses
- Contextually appropriate longer responses
- Pool of reasonable feedback text

#### Dropdowns/Select Menus
- Automatically detects available options
- Excludes empty placeholder options
- Random selection from valid options
- Proper option value handling

#### Number Inputs
- Respects min/max constraints
- Generates random numbers within valid range
- Handles range-based inputs (1-10, etc.)

### 3. Navigation Features

#### Multi-Page Support
- Automatically detects next/continue buttons
- Supports various button text patterns:
  - "Next", "Continue", "Submit"
  - "Finish", "Done", "Proceed"
  - Arrow symbols (">")
- Multiple selector strategies for buttons
- Configurable maximum pages
- Automatic progression through survey

#### Form Detection
- Multiple selector patterns for finding questions
- Deduplication of question elements
- Role-based element detection (ARIA)
- CSS class-based detection
- Data attribute detection

### 4. Configuration System

#### YAML Configuration
```yaml
selection_strategy: random
delay_between_questions: 1.0
delay_between_pages: 2.0
checkbox_check_probability: 0.5
preferred_responses:
  satisfaction: high
demographics:
  age: "25"
  country: "United States"
```

#### Programmatic Configuration
```python
config = SurveyConfig(
    selection_strategy='random',
    delay_between_questions=1.0,
    delay_between_pages=2.0,
    checkbox_check_probability=0.7,
    demographics={...}
)
```

### 5. Timing and Delays

#### Human-like Behavior
- Configurable delays between questions
- Configurable delays between pages
- Random variance in timing (0.5-1.5s per action)
- Wait for dynamic content loading
- Proper page load waiting

### 6. Browser Management

#### Headless Mode
- Run without visible browser window
- Faster execution
- Server-friendly

#### Headed Mode
- Visible browser for debugging
- Real-time observation
- Development and testing

#### Browser Configuration
- Custom viewport size (1280x720)
- Realistic user agent
- Context isolation
- Clean browser profile per session

### 7. Screenshot Capability
- Capture survey state at any point
- Completion verification
- PNG format output
- Custom filename support

### 8. Command-Line Interface

#### CLI Features
```bash
# Basic usage
python survey_cli.py https://example.com/survey

# With configuration file
python survey_cli.py URL -c config.yaml

# Headless mode
python survey_cli.py URL --headless

# Save screenshot
python survey_cli.py URL --screenshot result.png

# Verbose logging
python survey_cli.py URL -v

# Limit pages
python survey_cli.py URL -m 5

# Select strategy
python survey_cli.py URL -s first
```

### 9. Python API

#### Context Manager Support
```python
with SurveyFiller(config=config, headless=False) as filler:
    filler.fill_survey(url)
```

#### Manual Control
```python
filler = SurveyFiller(config=config)
filler.start_browser()
filler.navigate_to_survey(url)
# ... custom logic ...
filler.close_browser()
```

### 10. Error Handling

#### Graceful Degradation
- Continues on individual question errors
- Logs errors without crashing
- Skips problematic elements
- Returns partial success

#### Logging
- Configurable log levels
- Detailed operation logging
- Error tracking
- Progress reporting

### 11. Demographics Support

#### Profile-Based Responses
Pre-configured demographic data:
- Age
- Gender
- Country
- Employment status
- Education level
- Income range

#### Custom Demographics
Users can override defaults for personalized responses.

## Technical Features

### Architecture
- **Modular Design**: Separate concerns (config, handlers, main logic)
- **Extensible**: Easy to add new question types
- **Type Hints**: Full typing support for better IDE integration
- **Documentation**: Comprehensive docstrings

### Dependencies
- **Playwright**: Modern browser automation
- **PyYAML**: Configuration file support
- **Python 3.8+**: Modern Python features

### Code Quality
- UTF-8 encoding for cross-platform compatibility
- Proper logging practices (no global config in library)
- Configurable behavior (no hardcoded values)
- Clean separation of concerns
- Security-checked (CodeQL verified)

## Use Cases

### 1. Survey Testing
- Test survey platforms before deployment
- Verify form functionality
- Check multi-page flows
- Validate question types

### 2. Research Automation
- Automated data collection (where permitted)
- Batch survey completion
- Consistent response patterns

### 3. Platform Testing
- Test survey websites
- Verify browser compatibility
- Check responsive design
- Performance testing

### 4. Development Aid
- Rapid form testing during development
- QA automation
- Integration testing

## Limitations

### Current Limitations
1. **CAPTCHA**: Requires manual intervention
2. **Anti-bot Protection**: Some platforms may block automation
3. **Complex Conditional Logic**: May not handle all conditional flows
4. **JavaScript-heavy Surveys**: Some dynamic surveys may have issues
5. **Rate Limiting**: Platform rate limits may apply

### Not Supported
- File uploads (can be added in future)
- Drag-and-drop questions
- Drawing/sketching inputs
- Audio/video inputs
- Complex matrix questions (limited support)

## Future Enhancements

### Planned Features
- Advanced conditional logic handling
- Machine learning for better answer generation
- CAPTCHA solving integration
- More sophisticated timing patterns
- Session persistence
- Cookie management
- Proxy support
- Multi-browser support (Firefox, Safari)

### Potential Improvements
- Answer consistency checking
- Memory of previous answers
- Context-aware long-form responses
- Natural language generation
- Survey completion verification
- Detailed analytics
- Batch processing dashboard

## Security and Ethics

### Security Features
- No credential storage
- Clean browser profiles
- Safe file handling (UTF-8 encoding)
- No code injection vulnerabilities (CodeQL verified)

### Ethical Guidelines
✅ Use for legitimate testing
✅ Respect platform ToS
✅ Personal use where permitted
❌ Don't abuse reward systems
❌ Don't violate rate limits
❌ Don't use for fraud

## Performance

### Speed
- Headless mode: ~5-15 seconds per page
- Headed mode: ~10-20 seconds per page
- Configurable delays for customization

### Resource Usage
- Memory: ~200-300MB (browser + Python)
- CPU: Low (mostly I/O wait)
- Disk: Minimal (temporary browser profile)

## Compatibility

### Operating Systems
- ✅ Linux
- ✅ macOS
- ✅ Windows

### Python Versions
- ✅ Python 3.8+
- ✅ Python 3.9+
- ✅ Python 3.10+
- ✅ Python 3.11+
- ✅ Python 3.12+

### Browsers
- ✅ Chromium (primary)
- ⚠️ Firefox (via Playwright, not tested)
- ⚠️ WebKit (via Playwright, not tested)

## Documentation

### Available Documentation
- **README.md**: Project overview and quick start
- **USAGE.md**: Comprehensive usage guide
- **FEATURES.md**: This file - complete feature list
- **Inline Documentation**: Docstrings in all modules
- **Examples**: Multiple example scripts

## Support

### Getting Help
1. Check documentation (README, USAGE, FEATURES)
2. Review example scripts
3. Run with `-v` flag for detailed logging
4. Check GitHub issues
5. Create new issue with details

## Version

Current Version: 0.1.0

## License

MIT License - See LICENSE file for details.
