"""
Main Survey Filler class for automating survey completion
"""

import random
import time
import logging
from typing import Dict, List, Optional, Any
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from .question_handlers import QuestionHandler
from .config import SurveyConfig


logger = logging.getLogger(__name__)


class SurveyFiller:
    """
    Automated survey filler that can detect and complete various survey types.
    """

    def __init__(self, config: Optional[SurveyConfig] = None, headless: bool = False):
        """
        Initialize the survey filler.

        Args:
            config: Survey configuration with preferences
            headless: Whether to run browser in headless mode
        """
        self.config = config or SurveyConfig()
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.question_handler = QuestionHandler(self.config)

    def __enter__(self):
        """Context manager entry"""
        self.start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_browser()

    def start_browser(self):
        """Start the browser instance"""
        logger.info("Starting browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = self.context.new_page()
        logger.info("Browser started successfully")

    def close_browser(self):
        """Close the browser instance"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
        logger.info("Browser closed")

    def navigate_to_survey(self, url: str) -> bool:
        """
        Navigate to a survey URL.

        Args:
            url: The survey URL to navigate to

        Returns:
            True if navigation was successful
        """
        try:
            logger.info(f"Navigating to survey: {url}")
            self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)  # Wait for dynamic content
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to survey: {e}")
            return False

    def detect_survey_platform(self) -> str:
        """
        Detect which survey platform is being used.

        Returns:
            Platform identifier (e.g., 'qualtrics', 'surveymonkey', 'typeform', 'generic')
        """
        url = self.page.url.lower()
        
        if 'qualtrics' in url:
            return 'qualtrics'
        elif 'surveymonkey' in url:
            return 'surveymonkey'
        elif 'typeform' in url:
            return 'typeform'
        elif 'google.com/forms' in url:
            return 'google_forms'
        else:
            return 'generic'

    def find_survey_questions(self) -> List[Dict[str, Any]]:
        """
        Find all questions on the current page.

        Returns:
            List of question dictionaries with type and element information
        """
        questions = []
        seen_elements = set()
        
        # Look for various question patterns
        selectors = [
            'input[type="radio"]',
            'input[type="checkbox"]',
            'input[type="text"]',
            'textarea',
            'select',
            '[role="radiogroup"]',
            '[role="group"]',
            '.question',
            '[data-question]',
        ]

        for selector in selectors:
            elements = self.page.query_selector_all(selector)
            for element in elements:
                # Use element id to track if we've seen this element
                element_id = id(element)
                if element_id not in seen_elements:
                    question_info = self.question_handler.analyze_element(element)
                    if question_info:
                        questions.append(question_info)
                        seen_elements.add(element_id)

        logger.info(f"Found {len(questions)} questions on the page")
        return questions

    def fill_survey(self, url: str, max_pages: int = 20) -> bool:
        """
        Complete an entire survey from start to finish.

        Args:
            url: Survey URL to complete
            max_pages: Maximum number of pages to fill

        Returns:
            True if survey was completed successfully
        """
        if not self.navigate_to_survey(url):
            return False

        platform = self.detect_survey_platform()
        logger.info(f"Detected survey platform: {platform}")

        pages_filled = 0
        
        while pages_filled < max_pages:
            try:
                # Wait for page to be ready
                time.sleep(self.config.delay_between_questions)

                # Find and fill questions on current page
                questions = self.find_survey_questions()
                
                if not questions:
                    logger.info("No questions found on current page")
                    break

                for question in questions:
                    self.question_handler.handle_question(self.page, question)
                    time.sleep(random.uniform(0.5, 1.5))

                # Try to find and click next/submit button
                if not self.click_next_button():
                    logger.info("No next button found, survey may be complete")
                    break

                pages_filled += 1
                logger.info(f"Completed page {pages_filled}")
                time.sleep(self.config.delay_between_pages)

            except Exception as e:
                logger.error(f"Error filling survey page: {e}")
                break

        logger.info(f"Survey filling completed. Filled {pages_filled} pages.")
        return pages_filled > 0

    def click_next_button(self) -> bool:
        """
        Find and click the next/continue/submit button.

        Returns:
            True if button was found and clicked
        """
        # Common button selectors and text patterns
        button_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button.next',
            'button.continue',
            'a.next',
            '[data-action="next"]',
            '[data-action="submit"]',
        ]

        button_texts = ['next', 'continue', 'submit', 'finish', 'done', 'proceed', 'forward', '>']

        # Try direct selectors first
        for selector in button_selectors:
            try:
                button = self.page.query_selector(selector)
                if button and button.is_visible():
                    logger.info(f"Clicking next button: {selector}")
                    button.click()
                    time.sleep(2)
                    return True
            except Exception:
                continue

        # Try finding by text content
        for text in button_texts:
            try:
                button = self.page.get_by_role("button", name=text, exact=False)
                if button.count() > 0:
                    logger.info(f"Clicking button with text: {text}")
                    button.first.click()
                    time.sleep(2)
                    return True
            except Exception:
                continue

        return False

    def take_screenshot(self, filename: str = "survey_screenshot.png"):
        """
        Take a screenshot of the current page.

        Args:
            filename: Name of the screenshot file
        """
        try:
            self.page.screenshot(path=filename)
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
