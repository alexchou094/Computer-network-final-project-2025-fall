"""
Pre-Compile Analyzer
Provides smart hints by analyzing code before compilation
"""

from typing import Dict, List, Any
from .rules import (
    check_full_width,
    check_brackets,
    check_quotes,
    check_confusable,
)


class CodeAnalyzer:
    """
    Analyzes code for common syntax errors and style issues
    before compilation/execution
    """
    
    def __init__(self):
        self.rules = {
            'full_width': check_full_width,
            'brackets': check_brackets,
            'quotes': check_quotes,
            'confusable': check_confusable,
        }
    
    def analyze(self, code: str, rules_to_check: List[str] = None) -> Dict[str, Any]:
        """
        Analyze code using specified rules
        
        Args:
            code: Source code to analyze
            rules_to_check: List of rule names to check. If None, check all rules.
            
        Returns:
            Dictionary containing:
            - total_issues: Total number of issues found
            - issues_by_rule: Dictionary mapping rule names to their issues
            - summary: Human-readable summary
        """
        if rules_to_check is None:
            rules_to_check = list(self.rules.keys())
        
        issues_by_rule = {}
        total_issues = 0
        
        for rule_name in rules_to_check:
            if rule_name in self.rules:
                rule_func = self.rules[rule_name]
                issues = rule_func(code)
                issues_by_rule[rule_name] = issues
                total_issues += len(issues)
        
        # Generate summary
        summary = self._generate_summary(issues_by_rule, total_issues)
        
        return {
            'total_issues': total_issues,
            'issues_by_rule': issues_by_rule,
            'summary': summary,
        }
    
    def _generate_summary(self, issues_by_rule: Dict[str, List], total_issues: int) -> str:
        """Generate a human-readable summary of issues found"""
        if total_issues == 0:
            return "No issues found! Code looks good."
        
        summary_parts = [f"Found {total_issues} issue(s):"]
        
        for rule_name, issues in issues_by_rule.items():
            if issues:
                summary_parts.append(f"  - {rule_name}: {len(issues)} issue(s)")
        
        return "\n".join(summary_parts)
    
    def analyze_and_format(self, code: str, rules_to_check: List[str] = None) -> str:
        """
        Analyze code and return formatted output for display
        
        Args:
            code: Source code to analyze
            rules_to_check: List of rule names to check
            
        Returns:
            Formatted string with analysis results
        """
        result = self.analyze(code, rules_to_check)
        
        if result['total_issues'] == 0:
            return "✓ No issues found! Code looks good."
        
        output = [f"⚠ Found {result['total_issues']} issue(s):\n"]
        
        for rule_name, issues in result['issues_by_rule'].items():
            if not issues:
                continue
                
            output.append(f"\n{rule_name.upper().replace('_', ' ')}:")
            for issue in issues:
                line = issue.get('line', '?')
                col = issue.get('column', '?')
                msg = issue.get('message', 'Unknown issue')
                output.append(f"  Line {line}, Column {col}: {msg}")
                
                if 'suggestion' in issue:
                    output.append(f"    → Suggested fix: use '{issue['suggestion']}'")
        
        return "\n".join(output)


# Convenience function for quick analysis
def analyze_code(code: str, rules: List[str] = None) -> Dict[str, Any]:
    """
    Convenience function to analyze code
    
    Args:
        code: Source code to analyze
        rules: List of rule names to check
        
    Returns:
        Analysis results dictionary
    """
    analyzer = CodeAnalyzer()
    return analyzer.analyze(code, rules)
