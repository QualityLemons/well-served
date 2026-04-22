import json
from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError

class BaseTool(ABC):
    """
    The standard interface for all tools in the bank.
    Input -> Process -> Result
    """
    name = "Base Tool"
    description = ""
    version = "1.0"

    def __init__(self, user_input=None):
        self.user_input = user_input or {}
        self.errors = {}

    @abstractmethod
    def validate(self):
        """Check if user_input meets the tool's requirements."""
        pass

    @abstractmethod
    def process(self):
        """The core logic of the tool. Returns structured data."""
        pass

    def execute(self):
        """The pipeline runner used by the Django view."""
        self.validate()
        if self.errors:
            raise ValidationError(self.errors)
        
        return self.process()

    def get_metadata(self):
        """Consistent metadata for Tactics #6 and #8."""
        return {
            "tool_name": self.name,
            "version": self.version,
            "description": self.description,
        }