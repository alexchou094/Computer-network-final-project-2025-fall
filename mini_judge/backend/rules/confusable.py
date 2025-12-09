from typing import Dict, Optional

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
                "rule": "confusable",
                "message": "Found confusable unicode character.",
                "detail": f"Replace '{original}' with '{replacement}'.",
            }

    return None
