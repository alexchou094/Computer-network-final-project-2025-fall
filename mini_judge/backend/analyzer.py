from typing import Dict, List

from .rules import apply_rules


class Hint:
    """Simple hint container for static analysis results."""

    def __init__(self, rule: str, message: str, detail: str | None = None):
        self.rule = rule
        self.message = message
        self.detail = detail

    def to_dict(self) -> Dict[str, str]:
        payload = {"rule": self.rule, "message": self.message}
        if self.detail:
            payload["detail"] = self.detail
        return payload


def analyze_code(code: str) -> List[Dict[str, str]]:
    """
    Run static rules against the submitted code and return a list of hint dictionaries.
    """

    hints: List[Hint] = []
    for result in apply_rules(code):
        if result:
            hints.append(Hint(**result))

    return [hint.to_dict() for hint in hints]
