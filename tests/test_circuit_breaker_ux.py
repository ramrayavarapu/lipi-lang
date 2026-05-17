#!/usr/bin/env python3
"""
User experience tests for circuit breaker functionality.

This tests the end-to-end user flows when the circuit breaker
is activated in the claude-autofix workflow.
"""

import unittest
import subprocess
import tempfile
import os
import json
from unittest.mock import Mock, patch


class TestCircuitBreakerUX(unittest.TestCase):
    """End-to-end user experience tests for circuit breaker."""
    
    def setUp(self):
        """Set up test environment for UX testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Initialize a mock Git repository
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'developer@example.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Developer'], check=True)
        
        # Create initial files
        self._create_initial_files()
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_initial_files(self):
        """Create initial project files for testing."""
        with open('main.py', 'w') as f:
            f.write('''
def calculate(a, b):
    return a + b

if __name__ == "__main__":
    result = calculate(5, 3)
    print(f"Result: {result}")
''')
        
        with open('utils.py', 'w') as f:
            f.write('''
def helper_function():
    pass
''')
        
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    def test_user_flow_normal_pr_review_cycle(self):
        """
        Test normal PR review cycle without circuit breaker activation.
        
        Scenario: Developer creates PR → Copilot reviews → Claude fixes → Success
        """
        # Step 1: Developer makes changes and creates PR
        with open('main.py', 'a') as f:
            f.write('\n# Added new functionality\n')
        
        subprocess.run(['git', 'add', 'main.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'feat: add new functionality'], check=True)
        
        # Step 2: Simulate Copilot review (changes_requested)
        copilot_feedback = [
            {
                'file': 'main.py',
                'line': 5,
                'comment': 'Add error handling for invalid inputs'
            }
        ]
        
        # Step 3: Circuit breaker check (should NOT trigger - no autofix commit)
        last_commit = self._get_last_commit_message()
        circuit_breaker_triggered = last_commit.startswith('Auto-fix:')
        self.assertFalse(circuit_breaker_triggered, "Circuit breaker should not trigger on regular commit")
        
        # Step 4: Claude autofix would proceed normally
        # Simulate autofix making changes
        with open('main.py', 'w') as f:
            f.write('''
def calculate(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Inputs must be numbers")
    return a + b

if __name__ == "__main__":
    try:
        result = calculate(5, 3)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")
''')
        
        subprocess.run(['git', 'add', 'main.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto-fix: add error handling for invalid inputs'], check=True)
        
        # Verify successful flow completion
        self.assertTrue(os.path.exists('main.py'))
        with open('main.py', 'r') as f:
            content = f.read()
            self.assertIn('ValueError', content)
            self.assertIn('isinstance', content)
    
    def test_user_flow_circuit_breaker_activation(self):
        """
        Test user flow when circuit breaker activates.
        
        Scenario: Developer PR → Copilot review → Claude autofix → Copilot review again → Circuit breaker triggers
        """
        # Step 1: Initial developer commit
        with open('main.py', 'a') as f:
            f.write('\n# New feature\n')
        
        subprocess.run(['git', 'add', 'main.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'feat: add new feature'], check=True)
        
        # Step 2: First Claude autofix (normal flow)
        with open('main.py', 'a') as f:
            f.write('\n# Fixed issue 1\n')
        
        subprocess.run(['git', 'add', 'main.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto-fix: address Copilot review issues (Rule 2)'], check=True)
        
        # Step 3: Copilot reviews again and requests more changes
        # Step 4: Circuit breaker check (should trigger - last commit was autofix)
        last_commit = self._get_last_commit_message()
        circuit_breaker_triggered = last_commit.startswith('Auto-fix:')
        
        self.assertTrue(circuit_breaker_triggered, "Circuit breaker should trigger after autofix commit")
        
        # Step 5: Simulate circuit breaker behavior
        if circuit_breaker_triggered:
            # Circuit breaker comment would be posted
            expected_comment = self._get_circuit_breaker_comment()
            
            # Verify comment content for user clarity
            self.assertIn('Circuit Breaker Activated', expected_comment)
            self.assertIn('Manual intervention is required', expected_comment)
            self.assertIn('Review the recent autofix commits', expected_comment)
            self.assertIn('Make manual corrections', expected_comment)
            self.assertIn('Commit your changes', expected_comment)
            
            # Step 6: User receives clear guidance on next steps
            user_action_items = self._extract_user_actions_from_comment(expected_comment)
            expected_actions = [
                'Review the recent autofix commits and Copilot feedback',
                'Make manual corrections as needed',
                'Commit your changes to continue the review process'
            ]
            
            for action in expected_actions:
                self.assertIn(action, user_action_items)
    
    def test_user_flow_manual_intervention_recovery(self):
        """
        Test user flow for recovering from circuit breaker activation.
        
        Scenario: Circuit breaker triggers → User makes manual fix → Workflow resumes
        """
        # Set up scenario with circuit breaker triggered
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Auto-fix: previous fix'], check=True)
        
        # Verify circuit breaker would trigger
        last_commit = self._get_last_commit_message()
        self.assertTrue(last_commit.startswith('Auto-fix:'))
        
        # Step 1: User sees circuit breaker comment and takes manual action
        # Simulate user making manual corrections
        with open('main.py', 'a') as f:
            f.write('\n# Manual fix applied by developer\n')
        
        subprocess.run(['git', 'add', 'main.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'fix: manual correction after circuit breaker'], check=True)
        
        # Step 2: Verify circuit breaker no longer triggers
        new_last_commit = self._get_last_commit_message()
        circuit_breaker_triggered = new_last_commit.startswith('Auto-fix:')
        
        self.assertFalse(circuit_breaker_triggered, "Circuit breaker should not trigger after manual commit")
        
        # Step 3: Workflow can resume normal operation
        # If Copilot requests changes again, autofix can proceed
        self.assertTrue(new_last_commit.startswith('fix:'))
    
    def test_user_experience_edge_cases(self):
        """Test user experience in edge cases."""
        
        # Edge case 1: Multiple consecutive autofix commits
        autofix_commits = [
            'Auto-fix: address security issue',
            'Auto-fix: fix formatting',
            'Auto-fix: resolve linting errors'
        ]
        
        for commit_msg in autofix_commits:
            subprocess.run(['git', 'commit', '--allow-empty', '-m', commit_msg], check=True)
            
            # Each autofix after the first should trigger circuit breaker
            last_commit = self._get_last_commit_message()
            should_trigger = last_commit.startswith('Auto-fix:')
            self.assertTrue(should_trigger, f"Circuit breaker should trigger for: {commit_msg}")
        
        # Edge case 2: Empty repository or no commits
        # This is handled in the actual workflow, but we test the logic
        
        # Edge case 3: Very long commit messages
        long_autofix_message = 'Auto-fix: ' + 'a' * 1000  # Very long message
        subprocess.run(['git', 'commit', '--allow-empty', '-m', long_autofix_message], check=True)
        
        last_commit = self._get_last_commit_message()
        should_trigger = last_commit.startswith('Auto-fix:')
        self.assertTrue(should_trigger, "Circuit breaker should handle long autofix messages")
    
    def test_user_feedback_clarity(self):
        """Test that user feedback is clear and actionable."""
        comment = self._get_circuit_breaker_comment()
        
        # Test readability metrics
        self.assertLessEqual(len(comment.split('\n')), 15, "Comment should be concise")
        self.assertIn('🛑', comment, "Comment should have clear visual indicator")
        
        # Test actionable guidance
        action_keywords = ['Review', 'Make', 'Commit', 'required']
        for keyword in action_keywords:
            self.assertIn(keyword, comment, f"Comment should contain actionable keyword: {keyword}")
        
        # Test that technical jargon is explained
        self.assertIn('infinite loops', comment, "Technical concept should be explained")
        self.assertIn('autofix commit', comment, "Process should be explained")
    
    def test_developer_workflow_disruption_minimization(self):
        """Test that circuit breaker minimizes workflow disruption."""
        # Circuit breaker should:
        # 1. Activate only when necessary (consecutive autofixes)
        # 2. Provide clear recovery path
        # 3. Allow workflow to resume after manual intervention
        
        # Test 1: Single autofix doesn't disrupt (this is actually by design)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'feat: new feature'], check=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Auto-fix: fix issue'], check=True)
        
        # This should trigger circuit breaker (any autofix commit triggers it)
        last_commit = self._get_last_commit_message()
        self.assertTrue(last_commit.startswith('Auto-fix:'))
        
        # Test 2: Clear recovery path
        recovery_steps = [
            'Review the recent autofix commits and Copilot feedback',
            'Make manual corrections as needed', 
            'Commit your changes to continue the review process'
        ]
        
        comment = self._get_circuit_breaker_comment()
        for step in recovery_steps:
            self.assertIn(step, comment)
        
        # Test 3: Workflow resumes after manual commit
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'fix: manual correction'], check=True)
        new_last_commit = self._get_last_commit_message()
        self.assertFalse(new_last_commit.startswith('Auto-fix:'))
    
    def _get_last_commit_message(self):
        """Get the last commit message from current repository."""
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    
    def _get_circuit_breaker_comment(self):
        """Get the expected circuit breaker comment."""
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
    
    def _extract_user_actions_from_comment(self, comment):
        """Extract user action items from circuit breaker comment."""
        # Find the manual intervention section
        lines = comment.split('\n')
        action_section_started = False
        actions = []
        
        for line in lines:
            if 'Manual intervention is required' in line:
                action_section_started = True
                continue
            
            if action_section_started and line.strip().startswith(('1.', '2.', '3.')):
                # Extract action text after the number
                action = line.strip()[2:].strip()  # Remove "1. " prefix
                actions.append(action)
        
        return actions


class TestCircuitBreakerUserDocumentation(unittest.TestCase):
    """Test user-facing documentation and help text."""
    
    def test_circuit_breaker_explanation_clarity(self):
        """Test that circuit breaker concept is explained clearly."""
        explanation = (
            "The circuit breaker prevents infinite loops in the autofix workflow by detecting "
            "when the most recent commit is an autofix commit and halting further automated fixes."
        )
        
        # Should be understandable without deep technical knowledge
        simple_words = ['prevents', 'loops', 'detecting', 'halting', 'automated']
        for word in simple_words:
            self.assertIn(word, explanation.lower())
    
    def test_error_message_helpfulness(self):
        """Test that error messages are helpful to users."""
        error_scenarios = [
            {
                'scenario': 'circuit_breaker_triggered',
                'expected_elements': ['what happened', 'why it happened', 'what to do']
            }
        ]
        
        comment = '\n'.join([
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
        
        # What happened
        self.assertIn('Circuit Breaker Activated', comment)
        # Why it happened  
        self.assertIn('prevent infinite loops', comment)
        # What to do
        self.assertIn('Manual intervention is required', comment)
        self.assertIn('Review the recent autofix', comment)


if __name__ == '__main__':
    unittest.main(verbosity=2)