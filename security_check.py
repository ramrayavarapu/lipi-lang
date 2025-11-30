#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security scanner for lipi-lang codebase
Checks for common security vulnerabilities and malicious patterns
"""

import re
import sys
import os


class SecurityScanner:
    """Security vulnerability scanner"""

    def __init__(self):
        self.issues = []
        self.warnings = []

    def scan_file(self, filepath):
        """Scan a file for security issues"""
        print(f"🔍 Scanning {filepath}...")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Check for dangerous Python functions
        self._check_dangerous_functions(filepath, lines)

        # Check for code injection vulnerabilities
        self._check_code_injection(filepath, lines)

        # Check for command execution
        self._check_command_execution(filepath, lines)

        # Check for file operations
        self._check_file_operations(filepath, lines)

        # Check for network operations
        self._check_network_operations(filepath, lines)

        return len(self.issues) == 0

    def _check_dangerous_functions(self, filepath, lines):
        """Check for dangerous Python functions"""
        dangerous_patterns = [
            (r'\bexec\s*\(', 'exec() function usage'),
            (r'\b__import__\s*\((?!.*# allowed)', '__import__() usage'),
            (r'\bcompile\s*\(', 'compile() function usage'),
            (r'\bglobals\s*\(\)', 'globals() access'),
            (r'\blocals\s*\(\)', 'locals() manipulation'),
            (r'\bsetattr\s*\(', 'setattr() usage'),
            (r'\bdelattr\s*\(', 'delattr() usage'),
        ]

        for line_num, line in enumerate(lines, 1):
            # Skip comments and docstrings
            if line.strip().startswith('#') or '"""' in line:
                continue

            for pattern, description in dangerous_patterns:
                if re.search(pattern, line):
                    # Allow eval_lipi_expr function definition
                    if 'def eval_lipi_expr' in line or 'eval(' in line and 'eval_lipi_expr' in lines[max(0, line_num-5):line_num+5]:
                        continue

                    # Allow in test files if it's testing that injection is prevented (inside a string)
                    if 'test_' in filepath and ('"__import__' in line or "'__import__" in line):
                        continue

                    self.issues.append(
                        f"  ⚠️  {filepath}:{line_num}: Found {description}: {line.strip()}"
                    )

    def _check_code_injection(self, filepath, lines):
        """Check for potential code injection vulnerabilities"""
        injection_patterns = [
            (r'eval\s*\([^)]*\)', 'eval() with external input'),
        ]

        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                continue

            # Allow our eval_lipi_expr function
            if 'def eval_lipi_expr' in line:
                continue

            for pattern, description in injection_patterns:
                if re.search(pattern, line) and 'eval_lipi_expr' not in line:
                    # Check if it's our safe eval function
                    if 'eval_lipi_expr' not in ''.join(lines[max(0, line_num-2):line_num+2]):
                        self.warnings.append(
                            f"  ⚡ {filepath}:{line_num}: Potential {description}: {line.strip()}"
                        )

    def _check_command_execution(self, filepath, lines):
        """Check for command execution"""
        command_patterns = [
            (r'os\.system\s*\(', 'os.system() usage'),
            (r'os\.popen\s*\(', 'os.popen() usage'),
            (r'subprocess\.', 'subprocess module usage'),
            (r'commands\.', 'commands module usage'),
        ]

        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                continue

            for pattern, description in command_patterns:
                if re.search(pattern, line):
                    self.issues.append(
                        f"  🚫 {filepath}:{line_num}: Found {description}: {line.strip()}"
                    )

    def _check_file_operations(self, filepath, lines):
        """Check for potentially unsafe file operations"""
        file_patterns = [
            (r'open\s*\([^)]*["\']w["\']', 'File write operation'),
            (r'open\s*\([^)]*["\']a["\']', 'File append operation'),
            (r'os\.remove\s*\(', 'File deletion'),
            (r'os\.unlink\s*\(', 'File unlink operation'),
            (r'shutil\.rmtree\s*\(', 'Directory removal'),
        ]

        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                continue

            for pattern, description in file_patterns:
                if re.search(pattern, line):
                    # Allow if it's in test files or temporary files
                    if 'test_lipi.py' in filepath and 'temp' in line.lower():
                        continue

                    self.warnings.append(
                        f"  📝 {filepath}:{line_num}: Found {description}: {line.strip()}"
                    )

    def _check_network_operations(self, filepath, lines):
        """Check for network operations"""
        network_patterns = [
            (r'socket\.', 'Socket usage'),
            (r'urllib\.', 'URL operations'),
            (r'requests\.', 'HTTP requests'),
            (r'http\.client', 'HTTP client usage'),
        ]

        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                continue

            for pattern, description in network_patterns:
                if re.search(pattern, line):
                    self.issues.append(
                        f"  🌐 {filepath}:{line_num}: Found {description}: {line.strip()}"
                    )

    def print_report(self):
        """Print security scan report"""
        print("\n" + "="*60)
        print("SECURITY SCAN REPORT")
        print("="*60)

        if self.issues:
            print(f"\n❌ Found {len(self.issues)} CRITICAL issues:")
            for issue in self.issues:
                print(issue)
        else:
            print("\n✅ No critical security issues found!")

        if self.warnings:
            print(f"\n⚠️  Found {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(warning)
        else:
            print("\n✅ No warnings!")

        print("\n" + "="*60)

        return len(self.issues) == 0


def main():
    """Main security check function"""
    scanner = SecurityScanner()

    # Files to scan
    files_to_scan = [
        'lipi.py',
        'test_lipi.py',
    ]

    print("🛡️  Running security scan for lipi-lang\n")

    all_safe = True
    for filepath in files_to_scan:
        if os.path.exists(filepath):
            if not scanner.scan_file(filepath):
                all_safe = False
        else:
            print(f"⚠️  File not found: {filepath}")

    # Print final report
    success = scanner.print_report()

    if success:
        print("\n✅ Security scan PASSED\n")
        return 0
    else:
        print("\n❌ Security scan FAILED - Fix critical issues before committing\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
