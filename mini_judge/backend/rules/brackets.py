"""
Rule 2: Bracket matching detection
Detects unmatched brackets in code
"""


BRACKET_PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
}


def check_brackets(code: str) -> list[dict]:
    """
    Check for unmatched brackets in code
    
    Args:
        code: Source code string to check
        
    Returns:
        List of issues found, each containing:
        - line: line number (1-indexed)
        - column: column number (1-indexed)
        - char: the bracket character
        - message: error message
        - expected: expected closing bracket (if applicable)
    """
    issues = []
    stack = []  # Stack of (bracket, line, column)
    lines = code.split('\n')
    
    # Track if we're in a string literal
    in_single_quote = False
    in_double_quote = False
    
    for line_num, line in enumerate(lines, start=1):
        col_num = 0
        while col_num < len(line):
            char = line[col_num]
            
            # Handle escape sequences
            if col_num > 0 and line[col_num - 1] == '\\':
                col_num += 1
                continue
            
            # Toggle string state
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
            
            # Only check brackets outside of strings
            if not in_single_quote and not in_double_quote:
                if char in BRACKET_PAIRS:
                    # Opening bracket
                    stack.append((char, line_num, col_num + 1))
                elif char in BRACKET_PAIRS.values():
                    # Closing bracket
                    if not stack:
                        issues.append({
                            'line': line_num,
                            'column': col_num + 1,
                            'char': char,
                            'message': f'Unmatched closing bracket "{char}"'
                        })
                    else:
                        opening_bracket, open_line, open_col = stack.pop()
                        expected_closing = BRACKET_PAIRS[opening_bracket]
                        if char != expected_closing:
                            issues.append({
                                'line': line_num,
                                'column': col_num + 1,
                                'char': char,
                                'message': f'Mismatched bracket: expected "{expected_closing}" but found "{char}"',
                                'opening_line': open_line,
                                'opening_column': open_col,
                                'expected': expected_closing
                            })
                            # Put it back since it doesn't match
                            stack.append((opening_bracket, open_line, open_col))
            
            col_num += 1
    
    # Check for unclosed brackets
    while stack:
        opening_bracket, line_num, col_num = stack.pop()
        issues.append({
            'line': line_num,
            'column': col_num,
            'char': opening_bracket,
            'message': f'Unclosed opening bracket "{opening_bracket}"',
            'expected': BRACKET_PAIRS[opening_bracket]
        })
    
    return issues
