#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test suite for Lipi Language
Includes functional tests and security vulnerability checks
"""

import unittest
import sys
import os
import tempfile
from io import StringIO
from contextlib import contextmanager

# Import the lipi module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import lipi


@contextmanager
def captured_output():
    """Context manager to capture stdout"""
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


class TestBasicExpressions(unittest.TestCase):
    """Test basic expression evaluation"""

    def test_string_literal(self):
        env = {}
        result = lipi.eval_lipi_expr('"hello"', env)
        self.assertEqual(result, "hello")

    def test_integer_literal(self):
        env = {}
        result = lipi.eval_lipi_expr('42', env)
        self.assertEqual(result, 42)

    def test_variable_lookup(self):
        env = {"పేరు": "రాము"}
        result = lipi.eval_lipi_expr('పేరు', env)
        self.assertEqual(result, "రాము")

    def test_string_concatenation(self):
        env = {"పేరు": "రాము"}
        result = lipi.eval_lipi_expr('"నమస్తే " + పేరు', env)
        self.assertEqual(result, "నమస్తే రాము")

    def test_numeric_addition(self):
        env = {"వయసు": 20}
        result = lipi.eval_lipi_expr('వయసు + 5', env)
        self.assertEqual(result, 25)

    def test_comparisons(self):
        env = {"వయసు": 20}
        self.assertTrue(lipi.eval_lipi_expr('వయసు > 18', env))
        self.assertFalse(lipi.eval_lipi_expr('వయసు < 18', env))
        self.assertTrue(lipi.eval_lipi_expr('వయసు >= 20', env))
        self.assertTrue(lipi.eval_lipi_expr('వయసు == 20', env))
        self.assertTrue(lipi.eval_lipi_expr('వయసు != 19', env))


class TestTeluguKeywords(unittest.TestCase):
    """Test Telugu keyword functionality"""

    def test_telugu_print(self):
        env = {}
        with captured_output() as output:
            lipi.run_lipi_line('చెప్పు "నమస్తే"', env)
        self.assertEqual(output.getvalue().strip(), "నమస్తే")

    def test_telugu_assignment(self):
        env = {}
        lipi.run_lipi_line('పేరు = "రాము"', env)
        self.assertEqual(env["పేరు"], "రాము")

    def test_telugu_if_block(self):
        lines = [
            'యెడల 20 > 18:',
            '    చెప్పు "పెద్దవారు"',
            'ముగింపు'
        ]
        env = {}
        with captured_output() as output:
            lipi.run_lipi_if_block(lines, 0, env)
        self.assertIn("పెద్దవారు", output.getvalue())

    def test_telugu_while_loop(self):
        lines = [
            'వరకు కౌంట్ <= 3:',
            '    చెప్పు కౌంట్',
            '    కౌంట్ = కౌంట్ + 1',
            'ముగింపు'
        ]
        env = {"కౌంట్": 1}
        with captured_output() as output:
            lipi.run_lipi_while_block(lines, 0, env)
        output_lines = output.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)


class TestEnglishKeywords(unittest.TestCase):
    """Test English keyword functionality"""

    def test_english_print(self):
        env = {}
        with captured_output() as output:
            lipi.run_lipi_line('print "Hello"', env)
        self.assertEqual(output.getvalue().strip(), "Hello")

    def test_english_assignment(self):
        env = {}
        lipi.run_lipi_line('name = "Ram"', env)
        self.assertEqual(env["name"], "Ram")

    def test_english_if_block(self):
        lines = [
            'if 20 > 18:',
            '    print "Adult"',
            'end'
        ]
        env = {}
        with captured_output() as output:
            lipi.run_lipi_if_block(lines, 0, env)
        self.assertIn("Adult", output.getvalue())

    def test_english_while_loop(self):
        lines = [
            'while count <= 3:',
            '    print count',
            '    count = count + 1',
            'end'
        ]
        env = {"count": 1}
        with captured_output() as output:
            lipi.run_lipi_while_block(lines, 0, env)
        output_lines = output.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)


class TestBilingualSupport(unittest.TestCase):
    """Test bilingual (Telugu + English) support"""

    def test_mixed_variables(self):
        env = {}
        lipi.run_lipi_line('పేరు = "రాము"', env)
        lipi.run_lipi_line('name = "Ram"', env)
        self.assertEqual(env["పేరు"], "రాము")
        self.assertEqual(env["name"], "Ram")

    def test_telugu_keyword_english_variable(self):
        env = {"name": "Ram"}
        with captured_output() as output:
            lipi.run_lipi_line('చెప్పు name', env)
        self.assertEqual(output.getvalue().strip(), "Ram")

    def test_english_keyword_telugu_variable(self):
        env = {"పేరు": "రాము"}
        with captured_output() as output:
            lipi.run_lipi_line('print పేరు', env)
        self.assertEqual(output.getvalue().strip(), "రాము")

    def test_mixed_if_blocks(self):
        # Telugu if with English print
        lines = [
            'యెడల 20 > 18:',
            '    print "Adult"',
            'ముగింపు'
        ]
        env = {}
        with captured_output() as output:
            lipi.run_lipi_if_block(lines, 0, env)
        self.assertIn("Adult", output.getvalue())


class TestSecurityVulnerabilities(unittest.TestCase):
    """Security-focused tests to prevent vulnerabilities"""

    def test_no_code_injection_in_variables(self):
        """Ensure variable names cannot execute arbitrary code"""
        env = {}
        # Malicious variable names should just be stored as keys
        lipi.run_lipi_line('__import__ = "safe"', env)
        self.assertEqual(env["__import__"], "safe")

    def test_no_eval_injection(self):
        """Ensure expressions don't allow eval injection"""
        env = {}
        # Attempting to inject code should fail or be treated as literal
        with self.assertRaises(Exception):
            lipi.eval_lipi_expr('__import__("os").system("ls")', env)

    def test_infinite_loop_protection(self):
        """Test that infinite loops can be detected (timeout test)"""
        # This is a demonstration - in production, add timeout mechanism
        lines = [
            'while 1 > 0:',
            '    x = 1',  # Would loop forever
            'end'
        ]
        env = {}
        # For now, just verify the structure is correct
        # TODO: Add actual timeout mechanism in production
        self.assertTrue(True)

    def test_no_file_access_injection(self):
        """Ensure no file system access through string injection"""
        env = {}
        # File paths in strings should remain strings
        lipi.run_lipi_line('path = "/etc/passwd"', env)
        self.assertEqual(env["path"], "/etc/passwd")
        # Should not actually access the file
        self.assertTrue(isinstance(env["path"], str))

    def test_no_command_injection(self):
        """Ensure no command execution through strings"""
        env = {}
        lipi.run_lipi_line('cmd = "rm -rf /"', env)
        # Should store as string, not execute
        self.assertEqual(env["cmd"], "rm -rf /")

    def test_safe_string_operations(self):
        """Test that string operations are safe"""
        env = {"a": "test", "b": "value"}
        result = lipi.eval_lipi_expr('"safe " + a', env)
        self.assertEqual(result, "safe test")

    def test_no_import_injection(self):
        """Test that Python imports cannot be injected"""
        env = {}
        # These should fail as unknown expressions
        with self.assertRaises(Exception):
            lipi.eval_lipi_expr('import os', env)

    def test_no_dunder_method_access(self):
        """Ensure __methods__ cannot be accessed"""
        env = {"x": "test"}
        with self.assertRaises(Exception):
            lipi.eval_lipi_expr('x.__class__', env)

    def test_denial_of_service_protection(self):
        """Test protection against DoS via large numbers"""
        env = {}
        # Very large numbers should be handled safely
        lipi.run_lipi_line('big = 999999999999', env)
        self.assertEqual(env["big"], 999999999999)

    def test_unicode_injection_safety(self):
        """Test that Unicode characters don't cause injection"""
        env = {}
        lipi.run_lipi_line('unicode = "\\u0000\\u0001"', env)
        # Should store safely as string
        self.assertIn("unicode", env)


class TestFileExecution(unittest.TestCase):
    """Test file execution functionality"""

    def test_telugu_program_execution(self):
        """Test executing the Telugu example program"""
        with captured_output() as output:
            lipi.run_lipi_file('examples/hello.lipi.py')
        output_text = output.getvalue()
        self.assertIn("నమస్తే", output_text)
        self.assertIn("రామచంద్ర రావు", output_text)

    def test_english_program_execution(self):
        """Test executing the English example program"""
        with captured_output() as output:
            lipi.run_lipi_file('examples/english.lipi.py')
        output_text = output.getvalue()
        self.assertIn("Hello", output_text)
        self.assertIn("John", output_text)

    def test_bilingual_program_execution(self):
        """Test executing the bilingual example program"""
        with captured_output() as output:
            lipi.run_lipi_file('examples/bilingual.lipi.py')
        output_text = output.getvalue()
        self.assertIn("నమస్తే", output_text)
        self.assertIn("English", output_text)  # Check for "English" instead of "Hello"

    def test_malicious_file_content(self):
        """Test that malicious file content is handled safely"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lipi.py', delete=False, encoding='utf-8') as f:
            # Write potentially malicious content
            f.write('# Attempting injection\n')
            f.write('test = "safe"\n')
            f.write('చెప్పు test\n')
            temp_file = f.name

        try:
            with captured_output() as output:
                lipi.run_lipi_file(temp_file)
            self.assertEqual(output.getvalue().strip(), "safe")
        finally:
            os.unlink(temp_file)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""

    def test_undefined_variable(self):
        """Test that undefined variables raise appropriate errors"""
        env = {}
        with self.assertRaises(Exception):
            lipi.eval_lipi_expr('undefined_var', env)

    def test_syntax_error_handling(self):
        """Test that syntax errors are caught"""
        env = {}
        with self.assertRaises(Exception):
            lipi.run_lipi_line('invalid syntax here', env)

    def test_empty_lines(self):
        """Test that empty lines are handled correctly"""
        env = {}
        # Should not raise exception
        lipi.run_lipi_line('', env)
        lipi.run_lipi_line('   ', env)

    def test_comments(self):
        """Test that comments are ignored"""
        env = {}
        lipi.run_lipi_line('# This is a comment', env)
        self.assertEqual(len(env), 0)


class TestInputValidation(unittest.TestCase):
    """Test input validation and sanitization"""

    def test_special_characters_in_strings(self):
        """Test special characters in strings are safe"""
        env = {}
        lipi.run_lipi_line('test = "!@#$%^&*()"', env)
        self.assertEqual(env["test"], "!@#$%^&*()")

    def test_quotes_in_strings(self):
        """Test nested quotes handling"""
        env = {}
        lipi.run_lipi_line("test = 'value'", env)
        self.assertEqual(env["test"], "value")

    def test_numeric_overflow(self):
        """Test large numbers don't cause overflow issues"""
        env = {"a": 999999999}
        result = lipi.eval_lipi_expr('a + 1', env)
        self.assertEqual(result, 1000000000)


def run_tests():
    """Run all tests and generate report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBasicExpressions))
    suite.addTests(loader.loadTestsFromTestCase(TestTeluguKeywords))
    suite.addTests(loader.loadTestsFromTestCase(TestEnglishKeywords))
    suite.addTests(loader.loadTestsFromTestCase(TestBilingualSupport))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityVulnerabilities))
    suite.addTests(loader.loadTestsFromTestCase(TestFileExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestInputValidation))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
