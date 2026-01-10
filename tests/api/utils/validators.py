import re

class Validator:
    """Base class to identify custom validators in serializers."""
    pass

class Any(Validator):
    """Matches any non-None value of a specific type."""
    def __init__(self, expected_type=None):
        self.expected_type = expected_type

    def __eq__(self, other):
        if other is None:
            return False
        if self.expected_type and not isinstance(other, self.expected_type):
            return False
        return True

    def __repr__(self):
        if self.expected_type:
            return f"[Any {self.expected_type.__name__}]"
        return "[Any Value]"

class Regex(Validator):
    """Matches a string against a regex pattern."""
    def __init__(self, pattern, description=None):
        self.pattern = pattern
        # specific description helps in the Allure report (e.g. "<7-Digit ID>")
        self.description = description or f"Regex({pattern})"

    def __eq__(self, other):
        # Must be a string to match regex
        if not isinstance(other, str):
            return False
        # re.match checks for a match at the beginning of the string
        # Use ^...$ in your pattern to ensure full string match if needed
        return bool(re.match(self.pattern, other))

    def __repr__(self):
        return f"[{self.description}]"