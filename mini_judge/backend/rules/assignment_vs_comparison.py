import re
from typing import Dict, Optional

RULE_ID = "assignment_vs_comparison"
RULE_DESCRIPTION = "Detect possible accidental assignment ('=') inside conditionals; did you mean '=='?"


def _looks_like_assignment_in_condition(line: str) -> bool:
    """
    Heuristic: flag lines that contain '=' inside an if/while header but not comparison/walrus/compound ops.
    """
    header = line.split("#", 1)[0]  # ignore comments
    if not header.strip():
        return False

    # Only consider lines that start with an if/while header
    if not re.match(r"\s*(if|while)\b", header):
        return False

    # Skip comparison or walrus or compound assignment tokens
    skip_tokens = ["==", ":=", "<=", ">=", "!="]
    for tok in skip_tokens:
        header = header.replace(tok, "")

    # If a bare '=' remains, treat it as suspicious
    return "=" in header


def check_conditional_assignment_mistake(code: str) -> Optional[Dict[str, str]]:
    for idx, line in enumerate(code.splitlines(), start=1):
        if _looks_like_assignment_in_condition(line):
            return {
                "rule": RULE_ID,
                "message": "Possible accidental assignment inside conditional.",
                "detail": f"Line {idx}: {line.strip()}",
            }
    return None
