import re
from typing import Dict, Optional

RULE_ID = "full_width"
RULE_DESCRIPTION = "Check for full-width punctuation or symbols."

FULL_WIDTH_PATTERN = re.compile(r"[\uff01-\uff5e]")


def check_full_width_symbols(code: str) -> Optional[Dict[str, str]]:
    match = FULL_WIDTH_PATTERN.search(code)
    if not match:
        return None

    return {
        "rule": RULE_ID,
        "message": "Detected full-width punctuation or symbols.",
        "detail": f"Example: '{match.group()}'",
    }
