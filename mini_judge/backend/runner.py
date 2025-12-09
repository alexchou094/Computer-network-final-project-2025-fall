"""
Code Runner
Executes code locally and compares output with expected results
"""

import subprocess
import tempfile
import os
import time
from typing import Dict, Any, Optional, List
from pathlib import Path


class CodeRunner:
    """
    Runs code in a sandboxed environment and compares output
    """
    
    def __init__(self, timeout: int = 5):
        """
        Initialize the code runner
        
        Args:
            timeout: Maximum execution time in seconds
        """
        self.timeout = timeout
        self.supported_languages = {
            'python': {
                'extension': '.py',
                'command': ['python3'],
            },
            'cpp': {
                'extension': '.cpp',
                'command': ['g++', '-o'],
                'compile_first': True,
            },
            'c': {
                'extension': '.c',
                'command': ['gcc', '-o'],
                'compile_first': True,
            },
            'java': {
                'extension': '.java',
                'command': ['javac'],
                'compile_first': True,
            },
        }
    
    def run_code(
        self,
        code: str,
        language: str,
        test_input: str = "",
        expected_output: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run code and optionally compare with expected output
        
        Args:
            code: Source code to run
            language: Programming language (python, cpp, c, java)
            test_input: Input to provide to the program
            expected_output: Expected output for comparison
            
        Returns:
            Dictionary containing:
            - success: Whether execution succeeded
            - output: Program output
            - error: Error message if any
            - execution_time: Time taken to execute
            - match: Whether output matches expected (if expected_output provided)
        """
        if language not in self.supported_languages:
            return {
                'success': False,
                'error': f'Unsupported language: {language}. Supported: {list(self.supported_languages.keys())}',
                'output': '',
                'execution_time': 0,
            }
        
        lang_config = self.supported_languages[language]
        
        try:
            # Create temporary directory for code execution
            with tempfile.TemporaryDirectory() as tmpdir:
                # Write code to file
                source_file = os.path.join(tmpdir, f'code{lang_config["extension"]}')
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                # Compile if needed
                if lang_config.get('compile_first', False):
                    compile_result = self._compile_code(source_file, tmpdir, lang_config, language)
                    if not compile_result['success']:
                        return compile_result
                    executable = compile_result['executable']
                else:
                    executable = source_file
                
                # Execute code
                execution_result = self._execute_code(
                    executable,
                    tmpdir,
                    lang_config,
                    language,
                    test_input
                )
                
                # Compare output if expected output is provided
                if expected_output is not None:
                    execution_result['match'] = self._compare_output(
                        execution_result.get('output', ''),
                        expected_output
                    )
                    execution_result['expected_output'] = expected_output
                
                return execution_result
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'output': '',
                'execution_time': 0,
            }
    
    def _compile_code(
        self,
        source_file: str,
        tmpdir: str,
        lang_config: Dict,
        language: str
    ) -> Dict[str, Any]:
        """Compile code for languages that require compilation"""
        try:
            output_file = os.path.join(tmpdir, 'program')
            
            if language == 'java':
                # Java compilation
                result = subprocess.run(
                    [*lang_config['command'], source_file],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=tmpdir
                )
                # For Java, executable is the class file
                class_name = Path(source_file).stem
                executable = class_name
            else:
                # C/C++ compilation
                result = subprocess.run(
                    [*lang_config['command'], output_file, source_file],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=tmpdir
                )
                executable = output_file
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'Compilation error:\n{result.stderr}',
                    'output': '',
                    'execution_time': 0,
                }
            
            return {
                'success': True,
                'executable': executable,
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Compilation timeout (>{self.timeout}s)',
                'output': '',
                'execution_time': 0,
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Compilation error: {str(e)}',
                'output': '',
                'execution_time': 0,
            }
    
    def _execute_code(
        self,
        executable: str,
        tmpdir: str,
        lang_config: Dict,
        language: str,
        test_input: str
    ) -> Dict[str, Any]:
        """Execute the compiled or interpreted code"""
        try:
            start_time = time.time()
            
            # Prepare execution command
            if language == 'python':
                cmd = [*lang_config['command'], executable]
            elif language == 'java':
                cmd = ['java', executable]
            else:
                cmd = [executable]
            
            # Run the program
            result = subprocess.run(
                cmd,
                input=test_input,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=tmpdir
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode != 0 and result.stderr:
                return {
                    'success': False,
                    'error': f'Runtime error:\n{result.stderr}',
                    'output': result.stdout,
                    'execution_time': execution_time,
                }
            
            return {
                'success': True,
                'output': result.stdout,
                'error': result.stderr if result.stderr else None,
                'execution_time': execution_time,
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Execution timeout (>{self.timeout}s)',
                'output': '',
                'execution_time': self.timeout,
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution error: {str(e)}',
                'output': '',
                'execution_time': 0,
            }
    
    def _compare_output(self, actual: str, expected: str) -> Dict[str, Any]:
        """
        Compare actual output with expected output
        
        Returns:
            Dictionary with comparison results
        """
        # Normalize line endings
        actual_lines = actual.strip().split('\n')
        expected_lines = expected.strip().split('\n')
        
        # Exact match
        exact_match = actual.strip() == expected.strip()
        
        # Line by line comparison
        line_differences = []
        max_lines = max(len(actual_lines), len(expected_lines))
        
        for i in range(max_lines):
            actual_line = actual_lines[i] if i < len(actual_lines) else '<missing>'
            expected_line = expected_lines[i] if i < len(expected_lines) else '<missing>'
            
            if actual_line != expected_line:
                line_differences.append({
                    'line': i + 1,
                    'expected': expected_line,
                    'actual': actual_line,
                })
        
        return {
            'exact_match': exact_match,
            'line_differences': line_differences,
            'match_percentage': (1 - len(line_differences) / max_lines) * 100 if max_lines > 0 else 100,
        }
    
    def run_test_cases(
        self,
        code: str,
        language: str,
        test_cases: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Run multiple test cases
        
        Args:
            code: Source code
            language: Programming language
            test_cases: List of test cases, each with 'input' and 'expected_output'
            
        Returns:
            Results for all test cases
        """
        results = []
        passed = 0
        failed = 0
        
        for i, test_case in enumerate(test_cases):
            result = self.run_code(
                code,
                language,
                test_case.get('input', ''),
                test_case.get('expected_output')
            )
            result['test_case_id'] = i + 1
            results.append(result)
            
            if result.get('success') and result.get('match', {}).get('exact_match'):
                passed += 1
            else:
                failed += 1
        
        return {
            'total': len(test_cases),
            'passed': passed,
            'failed': failed,
            'results': results,
        }
