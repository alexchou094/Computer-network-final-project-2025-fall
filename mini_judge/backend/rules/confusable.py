import re
from typing import Dict, Optional, List

RULE_ID = "confusable"
RULE_ID_zh = "易混淆字元"
RULE_DESCRIPTION = "Detect visually confusable identifiers (e.g., I/l/1, O/0) that may cause confusion in code."

CONFUSABLE = {
    # Visually similar ASCII characters (identifiers & operators)
    "|": "l",
    "!": "1",
    "l": "1",
    "I": "1",
    "O": "0",
    "S": "5",
    "B": "8",
    "Z": "2",

    # Mathematical / operator lookalikes
    "-": "–",  # hyphen vs en-dash (visual confusion)
    "/": "1",  # division slash vs digit 1 in some fonts

    # Brackets that are visually similar in some fonts
    "(": "[",
    ")": "]",
    "[": "(",
    "]": ")",
    "{": "(",
    "}": ")",

    # Quotes / apostrophes (ASCII-level, not full-width)
    "'": "`",
    "`": "'",
}

# Identifier-level visually confusable groups
CONFUSABLE_IDENTIFIER_GROUPS = [
    {"I", "l", "1"},
    {"O", "0"},
]


def check_confusable_characters(code: str) -> Optional[Dict[str, str]]:
    # 1) Character-level unicode confusables (original behavior)
    for original, replacement in CONFUSABLE.items():
        if original in code:
            return {
                "rule": RULE_ID,
                "message": "Found confusable unicode character.",
                "detail": f"Replace '{original}' with '{replacement}'.",
            }

    # 2) Identifier-level confusable detection
    # Extract identifiers using a simple regex (language-agnostic heuristic)
    identifiers: List[str] = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", code)
    identifier_set = set(identifiers)

    for group in CONFUSABLE_IDENTIFIER_GROUPS:
        used = group & identifier_set
        if len(used) >= 2:
            return {
                "rule": RULE_ID,
                "message": "Found visually confusable identifiers.",
                "detail": (
                    f"Identifiers {sorted(used)} are visually similar and may cause confusion. "
                    "Consider renaming variables to more distinct names."
                ),
            }

    return None
