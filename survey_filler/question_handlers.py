"""
Question handlers for different survey question types
"""

import random
import logging
from typing import Dict, Any, Optional, List
from playwright.sync_api import Page, ElementHandle

logger = logging.getLogger(__name__)


class QuestionHandler:
    """
    Handles different types of survey questions (multiple choice, text, rating, etc.)
    """

    def __init__(self, config):
        """
        Initialize question handler.

        Args:
            config: Survey configuration
        """
        self.config = config

    def analyze_element(self, element: ElementHandle) -> Optional[Dict[str, Any]]:
        """
        Analyze an element to determine its question type.

        Args:
            element: The element to analyze

        Returns:
            Dictionary with question information or None
        """
        try:
            tag_name = element.evaluate("el => el.tagName.toLowerCase()")
            input_type = element.evaluate("el => el.type") if tag_name == 'input' else None

            question_info = {
                'element': element,
                'tag': tag_name,
                'type': input_type,
            }

            # Determine question type
            if tag_name == 'input':
                if input_type == 'radio':
                    question_info['question_type'] = 'radio'
                elif input_type == 'checkbox':
                    question_info['question_type'] = 'checkbox'
                elif input_type == 'text':
                    question_info['question_type'] = 'text'
                elif input_type == 'number':
                    question_info['question_type'] = 'number'
            elif tag_name == 'textarea':
                question_info['question_type'] = 'textarea'
            elif tag_name == 'select':
                question_info['question_type'] = 'select'
            else:
                return None

            return question_info

        except Exception as e:
            logger.debug(f"Error analyzing element: {e}")
            return None

    def handle_question(self, page: Page, question_info: Dict[str, Any]):
        """
        Handle a survey question based on its type.

        Args:
            page: The current page
            question_info: Question information dictionary
        """
        question_type = question_info.get('question_type')

        try:
            if question_type == 'radio':
                self.handle_radio_button(page, question_info)
            elif question_type == 'checkbox':
                self.handle_checkbox(page, question_info)
            elif question_type == 'text':
                self.handle_text_input(question_info)
            elif question_type == 'textarea':
                self.handle_textarea(question_info)
            elif question_type == 'select':
                self.handle_select(question_info)
            elif question_type == 'number':
                self.handle_number_input(question_info)
            else:
                logger.debug(f"Unknown question type: {question_type}")

        except Exception as e:
            logger.error(f"Error handling question: {e}")

    def handle_radio_button(self, page: Page, question_info: Dict[str, Any]):
        """
        Handle radio button questions by selecting one option.

        Args:
            page: The current page
            question_info: Question information
        """
        try:
            element = question_info['element']
            name = element.evaluate("el => el.name")
            
            if not name:
                return

            # Find all radio buttons with the same name
            radio_group = page.query_selector_all(f'input[type="radio"][name="{name}"]')
            
            if radio_group:
                # Filter only visible and enabled radio buttons
                visible_radios = [r for r in radio_group if r.is_visible() and r.is_enabled()]
                
                if visible_radios:
                    # Select a random option or based on preference
                    selected = self._select_radio_option(visible_radios)
                    if selected:
                        selected.click()
                        logger.info(f"Selected radio button from group: {name}")

        except Exception as e:
            logger.error(f"Error handling radio button: {e}")

    def _select_radio_option(self, options: List[ElementHandle]) -> Optional[ElementHandle]:
        """
        Select which radio option to choose based on strategy.

        Args:
            options: List of radio button options

        Returns:
            Selected option element
        """
        if not options:
            return None

        strategy = self.config.selection_strategy

        if strategy == 'random':
            return random.choice(options)
        elif strategy == 'first':
            return options[0]
        elif strategy == 'middle':
            return options[len(options) // 2]
        elif strategy == 'last':
            return options[-1]
        else:
            return random.choice(options)

    def handle_checkbox(self, page: Page, question_info: Dict[str, Any]):
        """
        Handle checkbox questions.

        Args:
            page: The current page
            question_info: Question information
        """
        try:
            element = question_info['element']
            
            # Check if already checked
            is_checked = element.is_checked()
            
            # Decide whether to check or uncheck based on strategy
            should_check = random.random() < 0.5  # 50% chance
            
            if should_check and not is_checked:
                element.click()
                logger.info("Checked checkbox")
            elif not should_check and is_checked:
                element.click()
                logger.info("Unchecked checkbox")

        except Exception as e:
            logger.error(f"Error handling checkbox: {e}")

    def handle_text_input(self, question_info: Dict[str, Any]):
        """
        Handle text input questions.

        Args:
            question_info: Question information
        """
        try:
            element = question_info['element']
            
            # Generate appropriate text based on field type/name
            text = self._generate_text_response(element)
            
            element.fill(text)
            logger.info(f"Filled text input with: {text}")

        except Exception as e:
            logger.error(f"Error handling text input: {e}")

    def _generate_text_response(self, element: ElementHandle) -> str:
        """
        Generate appropriate text response based on input context.

        Args:
            element: Input element

        Returns:
            Generated text
        """
        try:
            # Try to get field name or placeholder for context
            name = element.evaluate("el => el.name || ''").lower()
            placeholder = element.evaluate("el => el.placeholder || ''").lower()
            context = f"{name} {placeholder}"

            # Generate contextual responses
            if 'email' in context:
                return f"user{random.randint(1000, 9999)}@example.com"
            elif 'name' in context:
                names = ['John Doe', 'Jane Smith', 'Alex Johnson', 'Chris Williams']
                return random.choice(names)
            elif 'age' in context or 'old' in context:
                return str(random.randint(18, 65))
            elif 'phone' in context:
                return f"555-{random.randint(1000, 9999)}"
            elif 'city' in context:
                cities = ['New York', 'Los Angeles', 'Chicago', 'Houston']
                return random.choice(cities)
            elif 'country' in context:
                countries = ['United States', 'Canada', 'United Kingdom', 'Australia']
                return random.choice(countries)
            elif 'zip' in context or 'postal' in context:
                return f"{random.randint(10000, 99999)}"
            else:
                # Generic response
                responses = ['Yes', 'No', 'Maybe', 'Not sure', 'N/A']
                return random.choice(responses)

        except Exception:
            return 'Response'

    def handle_textarea(self, question_info: Dict[str, Any]):
        """
        Handle textarea questions.

        Args:
            question_info: Question information
        """
        try:
            element = question_info['element']
            
            # Generate longer text for textarea
            responses = [
                "This is a detailed response to the question.",
                "I think this is a good survey and I'm happy to participate.",
                "The product/service meets my expectations.",
                "I would recommend this to others.",
                "Overall, I'm satisfied with my experience.",
            ]
            
            text = random.choice(responses)
            element.fill(text)
            logger.info(f"Filled textarea with: {text[:50]}...")

        except Exception as e:
            logger.error(f"Error handling textarea: {e}")

    def handle_select(self, question_info: Dict[str, Any]):
        """
        Handle select/dropdown questions.

        Args:
            question_info: Question information
        """
        try:
            element = question_info['element']
            
            # Get all options
            options = element.evaluate("""
                el => Array.from(el.options).map(opt => opt.value).filter(v => v)
            """)
            
            if options:
                # Select a random option (skip first if it's a placeholder)
                if len(options) > 1:
                    selected = random.choice(options[1:] if options[0] == '' else options)
                else:
                    selected = options[0]
                
                element.select_option(selected)
                logger.info(f"Selected dropdown option: {selected}")

        except Exception as e:
            logger.error(f"Error handling select: {e}")

    def handle_number_input(self, question_info: Dict[str, Any]):
        """
        Handle number input questions.

        Args:
            question_info: Question information
        """
        try:
            element = question_info['element']
            
            # Get min/max if available
            min_val = element.evaluate("el => el.min || 1")
            max_val = element.evaluate("el => el.max || 10")
            
            try:
                min_val = int(min_val) if min_val else 1
                max_val = int(max_val) if max_val else 10
            except (ValueError, TypeError):
                min_val, max_val = 1, 10
            
            # Generate a number within range
            number = random.randint(min_val, max_val)
            element.fill(str(number))
            logger.info(f"Filled number input with: {number}")

        except Exception as e:
            logger.error(f"Error handling number input: {e}")
