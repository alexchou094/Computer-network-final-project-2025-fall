"""
Rule 4: Confusable character detection
Detects visually similar characters that might cause errors
"""

from typing import List, Dict, Any


# Confusable characters mapping
# Format: confusable -> (intended, description)
CONFUSABLE_CHARS = {
    # Latin vs Cyrillic
    'а': ('a', 'Cyrillic "а" (U+0430) looks like Latin "a" (U+0061)'),
    'е': ('e', 'Cyrillic "е" (U+0435) looks like Latin "e" (U+0065)'),
    'о': ('o', 'Cyrillic "о" (U+043E) looks like Latin "o" (U+006F)'),
    'р': ('p', 'Cyrillic "р" (U+0440) looks like Latin "p" (U+0070)'),
    'с': ('c', 'Cyrillic "с" (U+0441) looks like Latin "c" (U+0063)'),
    'х': ('x', 'Cyrillic "х" (U+0445) looks like Latin "x" (U+0078)'),
    'у': ('y', 'Cyrillic "у" (U+0443) looks like Latin "y" (U+0079)'),
    'А': ('A', 'Cyrillic "А" (U+0410) looks like Latin "A" (U+0041)'),
    'В': ('B', 'Cyrillic "В" (U+0412) looks like Latin "B" (U+0042)'),
    'Е': ('E', 'Cyrillic "Е" (U+0415) looks like Latin "E" (U+0045)'),
    'К': ('K', 'Cyrillic "К" (U+041A) looks like Latin "K" (U+004B)'),
    'М': ('M', 'Cyrillic "М" (U+041C) looks like Latin "M" (U+004D)'),
    'Н': ('H', 'Cyrillic "Н" (U+041D) looks like Latin "H" (U+0048)'),
    'О': ('O', 'Cyrillic "О" (U+041E) looks like Latin "O" (U+004F)'),
    'Р': ('P', 'Cyrillic "Р" (U+0420) looks like Latin "P" (U+0050)'),
    'С': ('C', 'Cyrillic "С" (U+0421) looks like Latin "C" (U+0043)'),
    'Т': ('T', 'Cyrillic "Т" (U+0422) looks like Latin "T" (U+0054)'),
    'Х': ('X', 'Cyrillic "Х" (U+0425) looks like Latin "X" (U+0058)'),
    
    # Greek letters
    'α': ('a', 'Greek "α" (alpha) looks like Latin "a"'),
    'β': ('B', 'Greek "β" (beta) might be confused with Latin "B"'),
    'ο': ('o', 'Greek "ο" (omicron) looks like Latin "o"'),
    'ν': ('v', 'Greek "ν" (nu) looks like Latin "v"'),
    
    # Zero-width and invisible characters
    '\u200b': ('', 'Zero-width space (U+200B)'),
    '\u200c': ('', 'Zero-width non-joiner (U+200C)'),
    '\u200d': ('', 'Zero-width joiner (U+200D)'),
    '\ufeff': ('', 'Zero-width no-break space/BOM (U+FEFF)'),
    
    # Mathematical and special symbols
    '−': ('-', 'Minus sign "−" (U+2212) looks like hyphen-minus "-" (U+002D)'),
    '‐': ('-', 'Hyphen "‐" (U+2010) vs hyphen-minus "-" (U+002D)'),
    '–': ('-', 'En dash "–" (U+2013) looks like hyphen-minus "-"'),
    '—': ('-', 'Em dash "—" (U+2014) looks like hyphen-minus "-"'),
    '×': ('*', 'Multiplication sign "×" (U+00D7) vs asterisk "*"'),
    '÷': ('/', 'Division sign "÷" (U+00F7) vs slash "/"'),
    
    # Quotation marks
    ''': ("'", "Right single quotation mark (U+2019) vs apostrophe (U+0027)"),
    ''': ("'", "Left single quotation mark (U+2018) vs apostrophe (U+0027)"),
    '"': ('"', "Left double quotation mark (U+201C) vs quotation mark (U+0022)"),
    '"': ('"', "Right double quotation mark (U+201D) vs quotation mark (U+0022)"),
    
    # Digits that look similar
    'Ⅰ': ('I', 'Roman numeral "Ⅰ" (U+2160) vs Latin "I"'),
    'Ⅴ': ('V', 'Roman numeral "Ⅴ" (U+2164) vs Latin "V"'),
    'Ⅹ': ('X', 'Roman numeral "Ⅹ" (U+2169) vs Latin "X"'),
    
    # Other confusables
    'ı': ('i', 'Dotless i "ı" (U+0131) vs Latin "i" (U+0069)'),
    'ℓ': ('l', 'Script l "ℓ" (U+2113) vs Latin "l" (U+006C)'),
}


def check_confusable(code: str) -> List[Dict[str, Any]]:
    """
    Check for confusable characters in code
    
    Args:
        code: Source code string to check
        
    Returns:
        List of issues found, each containing:
        - line: line number (1-indexed)
        - column: column number (1-indexed)
        - char: the confusable character found
        - suggestion: the intended character
        - message: error message with details
    """
    issues = []
    lines = code.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        for col_num, char in enumerate(line, start=1):
            if char in CONFUSABLE_CHARS:
                suggestion, description = CONFUSABLE_CHARS[char]
                issues.append({
                    'line': line_num,
                    'column': col_num,
                    'char': char,
                    'suggestion': suggestion,
                    'message': description,
                    'char_code': f'U+{ord(char):04X}'
                })
    
    return issues
