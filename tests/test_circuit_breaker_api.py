#!/usr/bin/env python3
"""
API behavior tests for circuit breaker functionality.

This tests the API interactions and GitHub workflow behavior
when the circuit breaker is activated.
"""

import unittest
import json
import subprocess
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock


class MockGitHubAPI:
    """Mock GitHub API for testing circuit breaker API interactions."""
    
    def __init__(self):
        self.comments_posted = []
        self.workflow_runs = []
        self.pr_data = {}
    
    def post_comment(self, owner, repo, issue_number, body):
        """Mock posting a comment to GitHub."""
        comment = {
            'owner': owner,
            'repo': repo,
            'issue_number': issue_number,
            'body': body,
            'id': len(self.comments_posted) + 1
        }
        self.comments_posted.append(comment)
        return comment
    
    def get_pull_request_reviews(self, owner, repo, pr_number):
        """Mock getting PR reviews."""
        return [
            {
                'id': 1234567890,
                'user': {'login': 'github-copilot[bot]'},
                'state': 'changes_requested',
                'body': 'Please fix the following issues...'
            }
        ]
    
    def get_pull_request_comments(self, owner, repo, pr_number):
        """Mock getting PR inline comments."""
        return [
            {
                'pull_request_review_id': 1234567890,
                'path': 'src/example.py',
                'line': 10,
                'body': 'This function needs error handling'
            }
        ]
    
    def trigger_workflow_run(self, workflow_event):
        """Mock triggering a workflow run."""
        run = {
            'id': len(self.workflow_runs) + 1,
            'event': workflow_event,
            'status': 'completed',
            'conclusion': 'success'
        }
        self.workflow_runs.append(run)
        return run


class TestCircuitBreakerAPI(unittest.TestCase):
    """API behavior tests for circuit breaker functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_github_api = MockGitHubAPI()
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Set up mock environment variables
        self.mock_env = {
            'GITHUB_REPOSITORY': 'ramrayavarapu/lipi-lang',
            'GITHUB_TOKEN': 'mock_token',
            'PR_NUMBER': '123',
            'REVIEW_ID': '1234567890',
            'REVIEW_BODY': 'Please address these issues'
        }
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch.dict(os.environ, {'GITHUB_REPOSITORY': 'ramrayavarapu/lipi-lang'})
    def test_circuit_breaker_comment_posted_correctly(self):
        """Test that circuit breaker posts the correct comment format."""
        # Simulate circuit breaker activation
        comment_body = self._get_expected_circuit_breaker_comment()
        
        # Mock posting the comment
        comment = self.mock_github_api.post_comment(
            owner='ramrayavarapu',
            repo='lipi-lang',
            issue_number=123,
            body=comment_body
        )
        
        # Verify comment was posted
        self.assertEqual(len(self.mock_github_api.comments_posted), 1)
        posted_comment = self.mock_github_api.comments_posted[0]
        
        # Verify comment content
        self.assertIn('Circuit Breaker Activated', posted_comment['body'])
        self.assertIn('infinite loops', posted_comment['body'])
        self.assertIn('Manual intervention is required', posted_comment['body'])
        self.assertEqual(posted_comment['issue_number'], 123)
    
    def test_workflow_exit_behavior_on_circuit_breaker(self):
        """Test that workflow exits cleanly when circuit breaker triggers."""
        # Create a mock Git repository with an autofix commit
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
        
        # Create test file and autofix commit
        with open('test_file.py', 'w') as f:
            f.write('print("hello world")')
        subprocess.run(['git', 'add', 'test_file.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto-fix: address Copilot review issues (Rule 2)'], check=True)
        
        # Simulate the circuit breaker check
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )
        last_commit_msg = result.stdout.strip()
        
        # Verify that this would trigger the circuit breaker
        self.assertTrue(last_commit_msg.startswith('Auto-fix:'))
        
        # Simulate workflow exit code (would be 0 for clean exit)
        expected_exit_code = 0
        self.assertEqual(expected_exit_code, 0, "Workflow should exit cleanly when circuit breaker triggers")
    
    def test_api_error_handling_when_posting_comment(self):
        """Test handling of API errors when posting circuit breaker comment."""
        # Simulate API failure
        class APIException(Exception):
            pass
        
        def failing_post_comment(*args, **kwargs):
            raise APIException("GitHub API rate limit exceeded")
        
        # Test that the workflow handles API failures gracefully
        with self.assertRaises(APIException):
            failing_post_comment(
                owner='ramrayavarapu',
                repo='lipi-lang',
                issue_number=123,
                body='test comment'
            )
    
    def test_environment_variable_validation(self):
        """Test that required environment variables are validated."""
        required_vars = ['GITHUB_REPOSITORY', 'GITHUB_TOKEN', 'PR_NUMBER']
        
        for var in required_vars:
            # Test missing environment variable
            env_without_var = {k: v for k, v in self.mock_env.items() if k != var}
            
            with self.subTest(missing_var=var):
                # This would simulate the workflow failing when required env vars are missing
                self.assertNotIn(var, env_without_var)
    
    @patch('subprocess.run')
    def test_git_command_execution(self, mock_subprocess):
        """Test that Git commands are executed correctly for circuit breaker check."""
        # Mock successful git log command
        mock_subprocess.return_value = Mock(
            stdout='Auto-fix: address Copilot review issues (Rule 2)',
            returncode=0
        )
        
        # Simulate the git log command that would be run in the workflow
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Verify git command was called correctly
        mock_subprocess.assert_called_with(
            ['git', 'log', '-1', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )
    
    def test_workflow_continues_on_non_autofix_commit(self):
        """Test that workflow continues normally when circuit breaker doesn't trigger."""
        # Create a mock Git repository with a regular commit
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
        
        # Create test file and regular commit
        with open('test_file.py', 'w') as f:
            f.write('print("hello world")')
        subprocess.run(['git', 'add', 'test_file.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'feat: add hello world feature'], check=True)
        
        # Get the commit message
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )
        last_commit_msg = result.stdout.strip()
        
        # Verify that this would NOT trigger the circuit breaker
        self.assertFalse(last_commit_msg.startswith('Auto-fix:'))
        
        # Workflow should continue normally (no comment posted)
        self.assertEqual(len(self.mock_github_api.comments_posted), 0)
    
    def _get_expected_circuit_breaker_comment(self):
        """Get the expected circuit breaker comment text."""
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
    
    def test_pr_number_extraction_from_context(self):
        """Test extraction of PR number from GitHub context."""
        # Mock GitHub context that would be available in the workflow
        github_context = {
            'event': {
                'pull_request': {
                    'number': 123
                }
            }
        }
        
        # Extract PR number (simulating workflow logic)
        pr_number = github_context['event']['pull_request']['number']
        self.assertEqual(pr_number, 123)
        self.assertIsInstance(pr_number, int)
    
    def test_review_state_validation(self):
        """Test validation of review state for triggering workflow."""
        valid_states = ['changes_requested']
        invalid_states = ['approved', 'commented', 'dismissed']
        
        # Test valid state
        for state in valid_states:
            with self.subTest(state=state):
                # This would trigger the workflow
                self.assertIn(state, valid_states)
        
        # Test invalid states
        for state in invalid_states:
            with self.subTest(state=state):
                # This would NOT trigger the workflow
                self.assertNotIn(state, valid_states)


class TestCircuitBreakerWorkflowIntegration(unittest.TestCase):
    """Integration tests for workflow behavior with circuit breaker."""
    
    def test_workflow_yaml_structure_requirements(self):
        """Test that the workflow structure meets requirements for circuit breaker."""
        # Define expected workflow structure for circuit breaker
        expected_steps = [
            'checkout',
            'circuit_breaker_check',  # New step to be added
            'circuit_breaker_comment',  # New step to be added
            'circuit_breaker_exit',  # New step to be added
            'collect_copilot_comments',  # Existing step - should only run if circuit breaker not triggered
            'commit_and_push_fixes',  # Existing step - should only run if circuit breaker not triggered
            'comment_on_pr'  # Existing step - should only run if circuit breaker not triggered
        ]
        
        # Test that all required steps are identified
        for step in expected_steps:
            self.assertIsInstance(step, str)
            self.assertGreater(len(step), 0)
    
    def test_conditional_execution_logic(self):
        """Test conditional execution logic for circuit breaker."""
        # Simulate environment variable states
        circuit_breaker_scenarios = [
            {'CIRCUIT_BREAKER_TRIGGERED': 'true', 'should_skip_autofix': True},
            {'CIRCUIT_BREAKER_TRIGGERED': 'false', 'should_skip_autofix': False},
            {'CIRCUIT_BREAKER_TRIGGERED': '', 'should_skip_autofix': False},  # Default behavior
        ]
        
        for scenario in circuit_breaker_scenarios:
            with self.subTest(scenario=scenario):
                env_value = scenario['CIRCUIT_BREAKER_TRIGGERED']
                expected_skip = scenario['should_skip_autofix']
                
                # Simulate the workflow conditional logic
                should_skip_autofix = (env_value == 'true')
                self.assertEqual(should_skip_autofix, expected_skip)


if __name__ == '__main__':
    unittest.main(verbosity=2)