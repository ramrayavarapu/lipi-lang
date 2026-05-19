#!/usr/bin/env python3
"""
Unit tests for circuit breaker functionality in claude-autofix workflow.

This tests the core logic for detecting consecutive autofix commits
and preventing infinite loops in the autofix workflow.
"""

import unittest
import subprocess
import tempfile
import os


class CircuitBreakerLogic:
    """
    Core circuit breaker logic that would be implemented in the workflow.
    This class encapsulates the detection logic for testing purposes.
    """
    
    @staticmethod
    def should_trigger_circuit_breaker(last_commit_message):
        """
        Determines if circuit breaker should activate based on last commit message.
        
        Args:
            last_commit_message (str): The most recent commit message
            
        Returns:
            bool: True if circuit breaker should trigger, False otherwise
        """
        if not last_commit_message:
            return False
            
        return last_commit_message.strip().startswith("Auto-fix:")
    
    @staticmethod
    def get_circuit_breaker_comment():
        """
        Returns the comment that should be posted when circuit breaker triggers.
        
        Returns:
            str: The circuit breaker comment text
        """
        return '\n'.join([
            '🛑 **Circuit Breaker Activated**',
            '',
            'The claude-autofix workflow has detected that the most recent commit is an autofix commit.',
            'To prevent infinite loops, the autofix process has been halted.',
            '',
            '**Manual intervention is required:**',
            '1. Review the recent autofix commits and Copilot feedback',
            '2. Make manual corrections as needed',
            '3. Commit your changes to continue the review process',
            '',
            'The autofix workflow will resume on your next commit.'
        ])


class TestCircuitBreakerUnit(unittest.TestCase):
    """Unit tests for circuit breaker detection logic."""
    
    def test_circuit_breaker_triggers_on_autofix_commit(self):
        """Test that circuit breaker triggers when last commit is an autofix."""
        test_cases = [
            "Auto-fix: address Copilot review issues (Rule 2)",
            "Auto-fix: fix formatting issues",
            "Auto-fix: resolve security vulnerabilities",
            "Auto-fix: update dependencies",
        ]
        
        for commit_msg in test_cases:
            with self.subTest(commit_msg=commit_msg):
                result = CircuitBreakerLogic.should_trigger_circuit_breaker(commit_msg)
                self.assertTrue(result, f"Circuit breaker should trigger for: {commit_msg}")
    
    def test_circuit_breaker_does_not_trigger_on_regular_commits(self):
        """Test that circuit breaker does not trigger for regular commits."""
        test_cases = [
            "feat: add new feature",
            "fix: resolve bug in parser",
            "docs: update README",
            "refactor: improve code structure",
            "test: add unit tests",
            "chore: update dependencies",
            "style: fix formatting",
            "perf: improve performance",
            "",  # Empty message
            "Manual fix: address review comments",
            "Auto fix without colon",  # Note: no colon after "Auto"
        ]
        
        for commit_msg in test_cases:
            with self.subTest(commit_msg=commit_msg):
                result = CircuitBreakerLogic.should_trigger_circuit_breaker(commit_msg)
                self.assertFalse(result, f"Circuit breaker should not trigger for: {commit_msg}")
    
    def test_circuit_breaker_case_sensitive(self):
        """Test that circuit breaker detection is case-sensitive."""
        test_cases = [
            "auto-fix: lowercase should not trigger",
            "AUTO-FIX: uppercase should not trigger",
            "Auto-Fix: mixed case should not trigger",
        ]
        
        for commit_msg in test_cases:
            with self.subTest(commit_msg=commit_msg):
                result = CircuitBreakerLogic.should_trigger_circuit_breaker(commit_msg)
                self.assertFalse(result, f"Circuit breaker should not trigger for: {commit_msg}")
    
    def test_circuit_breaker_with_whitespace(self):
        """Test that circuit breaker handles whitespace correctly."""
        test_cases = [
            "  Auto-fix: with leading spaces",
            "Auto-fix: with trailing spaces  ",
            "\nAuto-fix: with newline prefix",
            "Auto-fix: normal message\n",
        ]
        
        for commit_msg in test_cases:
            with self.subTest(commit_msg=commit_msg):
                result = CircuitBreakerLogic.should_trigger_circuit_breaker(commit_msg)
                self.assertTrue(result, f"Circuit breaker should trigger for: {repr(commit_msg)}")
    
    def test_get_circuit_breaker_comment_content(self):
        """Test that circuit breaker comment contains required elements."""
        comment = CircuitBreakerLogic.get_circuit_breaker_comment()
        
        # Check for key elements in the comment
        required_elements = [
            "Circuit Breaker Activated",
            "infinite loops",
            "Manual intervention is required",
            "Review the recent autofix commits",
            "Make manual corrections",
            "Commit your changes",
        ]
        
        for element in required_elements:
            self.assertIn(element, comment, f"Comment should contain: {element}")
    
    def test_none_and_empty_commit_messages(self):
        """Test handling of None and empty commit messages."""
        test_cases = [None, "", "   ", "\n", "\t"]
        
        for commit_msg in test_cases:
            with self.subTest(commit_msg=repr(commit_msg)):
                result = CircuitBreakerLogic.should_trigger_circuit_breaker(commit_msg)
                self.assertFalse(result, f"Circuit breaker should not trigger for: {repr(commit_msg)}")


class TestCircuitBreakerGitIntegration(unittest.TestCase):
    """Integration tests using actual Git operations."""
    
    def setUp(self):
        """Set up temporary Git repository for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Initialize git repo
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
        
        # Create initial commit
        with open('test_file.txt', 'w') as f:
            f.write('initial content')
        subprocess.run(['git', 'add', 'test_file.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    def tearDown(self):
        """Clean up temporary directory."""
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def get_last_commit_message(self):
        """Helper to get the last commit message from current repo."""
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%s'],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    
    def test_git_integration_with_autofix_commit(self):
        """Test circuit breaker logic with real Git autofix commit."""
        # Create an autofix commit
        with open('test_file.txt', 'w') as f:
            f.write('autofix content')
        subprocess.run(['git', 'add', 'test_file.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto-fix: address Copilot review issues (Rule 2)'], check=True)
        
        last_commit_msg = self.get_last_commit_message()
        should_trigger = CircuitBreakerLogic.should_trigger_circuit_breaker(last_commit_msg)
        
        self.assertTrue(should_trigger, "Circuit breaker should trigger after autofix commit")
    
    def test_git_integration_with_regular_commit(self):
        """Test circuit breaker logic with regular commit."""
        # Create a regular commit
        with open('test_file.txt', 'w') as f:
            f.write('regular content')
        subprocess.run(['git', 'add', 'test_file.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', 'feat: add new functionality'], check=True)
        
        last_commit_msg = self.get_last_commit_message()
        should_trigger = CircuitBreakerLogic.should_trigger_circuit_breaker(last_commit_msg)
        
        self.assertFalse(should_trigger, "Circuit breaker should not trigger after regular commit")
    
    def test_consecutive_autofix_detection(self):
        """Test that the circuit breaker triggers when the latest commit is an Auto-fix commit."""
        # First autofix commit
        with open('test_file.txt', 'w') as f:
            f.write('first autofix')
        subprocess.run(['git', 'add', 'test_file.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto-fix: first fix'], check=True)
        
        # Second autofix commit (last commit is still "Auto-fix:", so circuit breaker triggers)
        with open('test_file.txt', 'w') as f:
            f.write('second autofix')
        subprocess.run(['git', 'add', 'test_file.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto-fix: second fix'], check=True)
        
        last_commit_msg = self.get_last_commit_message()
        should_trigger = CircuitBreakerLogic.should_trigger_circuit_breaker(last_commit_msg)
        
        self.assertTrue(should_trigger, "Circuit breaker should trigger when last commit is an Auto-fix commit")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)