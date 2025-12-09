import re
from typing import Dict, Optional

FULL_WIDTH_PATTERN = re.compile(r"[\uff01-\uff5e]")


def check_full_width_symbols(code: str) -> Optional[Dict[str, str]]:
    match = FULL_WIDTH_PATTERN.search(code)
    if not match:
        return None

    return {
        "rule": "full_width",
        "message": "Detected full-width punctuation or symbols.",
        "detail": f"Example: '{match.group()}'",
    }
