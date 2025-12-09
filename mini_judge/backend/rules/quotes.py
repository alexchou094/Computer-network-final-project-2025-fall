"""
Rule 3: Quote closure detection
Detects unclosed quotes in code
"""


def check_quotes(code: str) -> list[dict]:
    """
    Check for unclosed quotes in code
    
    Args:
        code: Source code string to check
        
    Returns:
        List of issues found, each containing:
        - line: line number (1-indexed)
        - column: column number (1-indexed)
        - char: the quote character
        - message: error message
    """
    issues = []
    lines = code.split('\n')
    
    # Track unclosed quotes
    single_quote_open = None  # (line, column)
    double_quote_open = None  # (line, column)
    
    for line_num, line in enumerate(lines, start=1):
        col_num = 0
        while col_num < len(line):
            char = line[col_num]
            
            # Handle escape sequences
            if col_num > 0 and line[col_num - 1] == '\\':
                col_num += 1
                continue
            
            if char == "'":
                if double_quote_open is None:  # Not inside double quotes
                    if single_quote_open is None:
                        # Opening single quote
                        single_quote_open = (line_num, col_num + 1)
                    else:
                        # Closing single quote
                        single_quote_open = None
            
            elif char == '"':
                if single_quote_open is None:  # Not inside single quotes
                    if double_quote_open is None:
                        # Opening double quote
                        double_quote_open = (line_num, col_num + 1)
                    else:
                        # Closing double quote
                        double_quote_open = None
            
            col_num += 1
        
        # At end of line, check if quotes are still open (might be multi-line strings in some languages)
        # For basic checking, we'll allow multi-line strings with triple quotes in Python
        # but flag unclosed single/double quotes at end of file
    
    # Check for unclosed quotes at the end of the file
    if single_quote_open is not None:
        line_num, col_num = single_quote_open
        issues.append({
            'line': line_num,
            'column': col_num,
            'char': "'",
            'message': 'Unclosed single quote'
        })
    
    if double_quote_open is not None:
        line_num, col_num = double_quote_open
        issues.append({
            'line': line_num,
            'column': col_num,
            'char': '"',
            'message': 'Unclosed double quote'
        })
    
    return issues
