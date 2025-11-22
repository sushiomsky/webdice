"""
Configuration for survey filler
"""

import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class SurveyConfig:
    """
    Configuration for survey filling behavior
    """
    
    # Selection strategies: 'random', 'first', 'middle', 'last'
    selection_strategy: str = 'random'
    
    # Delays (in seconds)
    delay_between_questions: float = 1.0
    delay_between_pages: float = 2.0
    
    # Checkbox selection probability (0.0 to 1.0)
    checkbox_check_probability: float = 0.5
    
    # User preferences
    preferred_responses: Dict[str, Any] = field(default_factory=dict)
    
    # Demographics (used for profile-based questions)
    demographics: Dict[str, str] = field(default_factory=lambda: {
        'age': '25',
        'country': 'United States',
        'employment': 'Employed',
    })
    
    @classmethod
    def from_yaml(cls, file_path: str) -> 'SurveyConfig':
        """
        Load configuration from YAML file.
        
        Args:
            file_path: Path to YAML configuration file
            
        Returns:
            SurveyConfig instance
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
        
        return cls(**config_dict)
    
    def to_yaml(self, file_path: str):
        """
        Save configuration to YAML file.
        
        Args:
            file_path: Path to save YAML configuration
        """
        config_dict = {
            'selection_strategy': self.selection_strategy,
            'delay_between_questions': self.delay_between_questions,
            'delay_between_pages': self.delay_between_pages,
            'checkbox_check_probability': self.checkbox_check_probability,
            'preferred_responses': self.preferred_responses,
            'demographics': self.demographics,
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False)
