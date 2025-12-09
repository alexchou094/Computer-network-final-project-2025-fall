from typing import Dict, Optional

PAIRS = {')': '(', ']': '[', '}': '{'}
OPENING = set(PAIRS.values())


def check_unbalanced_brackets(code: str) -> Optional[Dict[str, str]]:
    stack: list[str] = []
    for index, char in enumerate(code):
        if char in OPENING:
            stack.append(char)
        elif char in PAIRS:
            if not stack or stack[-1] != PAIRS[char]:
                return {
                    "rule": "brackets",
                    "message": "Unbalanced brackets detected.",
                    "detail": f"Unexpected '{char}' at position {index}",
                }
            stack.pop()

    if stack:
        return {
            "rule": "brackets",
            "message": "Bracket not closed.",
            "detail": f"Missing closing bracket for '{stack[-1]}'",
        }

    return None
