"""
Rule 1: Full-width symbol detection
Detects full-width symbols that should be half-width in code
"""

from typing import List, Dict, Any
import re


# Common full-width symbols that should be half-width in code
FULL_WIDTH_MAPPINGS = {
    '（': '(',
    '）': ')',
    '｛': '{',
    '｝': '}',
    '［': '[',
    '］': ']',
    '；': ';',
    '：': ':',
    '，': ',',
    '．': '.',
    '！': '!',
    '？': '?',
    '＝': '=',
    '＋': '+',
    '－': '-',
    '＊': '*',
    '／': '/',
    '＜': '<',
    '＞': '>',
    '＆': '&',
    '｜': '|',
    '＾': '^',
    '％': '%',
    '＄': '$',
    '＃': '#',
    '＠': '@',
    '　': ' ',  # Full-width space
}


def check_full_width(code: str) -> List[Dict[str, Any]]:
    """
    Check for full-width symbols in code
    
    Args:
        code: Source code string to check
        
    Returns:
        List of issues found, each containing:
        - line: line number (1-indexed)
        - column: column number (1-indexed)
        - char: the full-width character found
        - suggestion: the half-width replacement
        - message: error message
    """
    issues = []
    lines = code.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        for col_num, char in enumerate(line, start=1):
            if char in FULL_WIDTH_MAPPINGS:
                issues.append({
                    'line': line_num,
                    'column': col_num,
                    'char': char,
                    'suggestion': FULL_WIDTH_MAPPINGS[char],
                    'message': f'Full-width symbol "{char}" found, should use "{FULL_WIDTH_MAPPINGS[char]}"'
                })
    
    return issues
