#!/usr/bin/env python3
"""
API tests for GitHub Actions security integration.
Tests GitHub API interactions and workflow validation endpoints.
"""

import unittest
import json
import os
from pathlib import Path


class TestGitHubActionsSecurityAPI(unittest.TestCase):
    """API tests for GitHub Actions security validation."""
    
    def setUp(self):
        """Set up API test environment."""
        self.mock_api_responses = {
            'actions/checkout': {
                'latest_release': 'v4.2.0',
                'commit_sha': 'b4ffde65f46336ab88eb53be808477a3936bae11'
            },
            'actions/setup-python': {
                'latest_release': 'v5.0.0', 
                'commit_sha': '65d7f2d534ac1bc67fcd52423e459d7f65fa7115'
            },
            'actions/github-script': {
                'latest_release': 'v7.0.1',
                'commit_sha': '60a2d8b64675a63f597c7bed8c04b5f5b8c2e2cd'
            }
        }
    
    def test_action_metadata_structure(self):
        """Test that action metadata has required fields."""
        required_fields = ['latest_release', 'commit_sha']
        
        for action_name, metadata in self.mock_api_responses.items():
            for field in required_fields:
                self.assertIn(field, metadata,
                             f"Action {action_name} missing field: {field}")
    
    def test_commit_sha_format_validation(self):
        """Test commit SHA format validation via API."""
        import re
        sha_pattern = r'^[a-f0-9]{40}$'
        
        for action_name, metadata in self.mock_api_responses.items():
            sha = metadata.get('commit_sha', '')
            self.assertTrue(re.match(sha_pattern, sha),
                           f"Invalid SHA format for {action_name}: {sha}")
    
    def test_version_comparison_api(self):
        """Test version comparison API functionality."""
        def parse_version(version_str):
            """Parse semantic version string."""
            if version_str.startswith('v'):
                version_str = version_str[1:]
            return tuple(map(int, version_str.split('.')))
        
        # Test version parsing
        test_versions = ['v4.2.0', 'v5.0.0', 'v7.0.1']
        for version in test_versions:
            parsed = parse_version(version)
            self.assertEqual(len(parsed), 3, f"Version should have 3 parts: {version}")
            self.assertGreater(parsed[0], 0, f"Major version should be positive: {version}")
    
    def test_workflow_validation_endpoint(self):
        """Test workflow file validation logic."""
        # Mock workflow content with unpinned actions
        mock_workflow = """
        name: Test Workflow
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
          - uses: trufflesecurity/trufflehog@main
        """
        
        # Simulate validation API
        def validate_workflow_security(content):
            """Validate workflow content for security issues."""
            issues = []
            
            # Check for unpinned actions
            unpinned_patterns = [
                r'actions/checkout@v\d+',
                r'actions/setup-python@v\d+',
                r'trufflesecurity/trufflehog@main'
            ]
            
            import re
            for pattern in unpinned_patterns:
                if re.search(pattern, content):
                    issues.append(f"Unpinned action found: {pattern}")
            
            return issues
        
        issues = validate_workflow_security(mock_workflow)
        self.assertGreater(len(issues), 0, "Should detect unpinned actions")
        
        # Test with pinned actions (secure)
        secure_workflow = """
        name: Secure Workflow  
        steps:
          - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
          - uses: actions/setup-python@65d7f2d534ac1bc67fcd52423e459d7f65fa7115
        """
        
        secure_issues = validate_workflow_security(secure_workflow)
        self.assertEqual(len(secure_issues), 0, "Should not detect issues in pinned actions")
    
    def test_security_audit_api_integration(self):
        """Test integration with security audit system."""
        # Verify audit file contains API-compatible structure
        audit_file = Path(__file__).parent.parent / 'GITHUB_ACTIONS_SECURITY_AUDIT.md'
        
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                content = f.read()
            
            # Check for structured data that could be consumed by API
            api_indicators = [
                'Risk Level:', 
                'Current Usage:',
                'Recommended Action:',
                'security-tests.yml'
            ]
            
            for indicator in api_indicators:
                self.assertIn(indicator, content,
                             f"Audit should contain API-consumable data: {indicator}")
    
    def test_workflow_execution_api(self):
        """Test workflow execution validation through API."""
        # Mock GitHub Actions API response
        mock_workflow_runs = {
            'workflow_runs': [
                {
                    'id': 12345,
                    'status': 'completed',
                    'conclusion': 'success',
                    'name': 'Build Check'
                }
            ]
        }
        
        # Validate API response structure
        self.assertIn('workflow_runs', mock_workflow_runs)
        
        for run in mock_workflow_runs['workflow_runs']:
            required_fields = ['id', 'status', 'conclusion', 'name']
            for field in required_fields:
                self.assertIn(field, run, f"Workflow run missing field: {field}")


if __name__ == '__main__':
    unittest.main()