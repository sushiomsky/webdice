"""
Automated Survey Filler
A tool for automatically completing surveys on platforms like freecash.com
"""

from .survey_filler import SurveyFiller
from .question_handlers import QuestionHandler

__version__ = "0.1.0"
__all__ = ["SurveyFiller", "QuestionHandler"]
