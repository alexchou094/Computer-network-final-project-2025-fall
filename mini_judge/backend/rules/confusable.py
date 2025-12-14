from typing import Dict, Optional

RULE_ID = "confusable"
RULE_DESCRIPTION = "Check for confusable unicode characters."

CONFUSABLE = {
    "；": ";",
    "，": ",",
    "＃": "#",
    "＄": "$",
    "／": "/",
    "＼": "\\",
    "＂": '"',
    "＇": "'",
    "﹣": "-",
}


def check_confusable_characters(code: str) -> Optional[Dict[str, str]]:
    for original, replacement in CONFUSABLE.items():
        if original in code:
            return {
                "rule": RULE_ID,
                "message": "Found confusable unicode character.",
                "detail": f"Replace '{original}' with '{replacement}'.",
            }

    return None
