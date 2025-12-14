from typing import Dict, Optional

RULE_ID = "quotes"
RULE_DESCRIPTION = "Check for unclosed quotes."

QUOTES = {'"', "'"}


def check_unclosed_quotes(code: str) -> Optional[Dict[str, str]]:
    stack: list[str] = []
    escaped = False
    for index, char in enumerate(code):
        if escaped:
            escaped = False
            continue

        if char == "\\":
            escaped = True
            continue

        if char in QUOTES:
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)

    if stack:
        return {
            "rule": RULE_ID,
            "message": "Quote not closed.",
            "detail": f"Unclosed quote starting with '{stack[-1]}'",
        }

    return None
