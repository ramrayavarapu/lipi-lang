#!/usr/bin/env python3
"""
Unit tests for GitHub Actions security pinning validation.
Tests ensure workflow files use commit SHAs instead of version tags.
"""

import unittest
import os
import re
from pathlib import Path


class TestGitHubActionsSecurity(unittest.TestCase):
    """Unit tests for GitHub Actions version pinning security."""
    
    def setUp(self):
        """Set up test environment."""
        self.workflows_dir = Path(__file__).parent.parent / '.github' / 'workflows'
        self.target_actions = {
            'actions/checkout': r'actions/checkout@v\d+',
            'actions/setup-python': r'actions/setup-python@v\d+', 
            'actions/github-script': r'actions/github-script@v\d+',
            'trufflesecurity/trufflehog': r'trufflesecurity/trufflehog@main'
        }
    
    def test_workflow_directory_exists(self):
        """Test that workflows directory exists."""
        self.assertTrue(self.workflows_dir.exists(), 
                       f"Workflows directory not found: {self.workflows_dir}")
    
    def test_detect_unpinned_actions(self):
        """Test detection of unpinned GitHub Actions."""
        unpinned_actions = []
        
        if not self.workflows_dir.exists():
            self.skipTest("Workflows directory not found")
            
        for workflow_file in self.workflows_dir.glob('*.yml'):
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            for action_name, pattern in self.target_actions.items():
                matches = re.findall(pattern, content)
                if matches:
                    unpinned_actions.append({
                        'file': workflow_file.name,
                        'action': action_name,
                        'matches': matches
                    })
        
        # Document findings for security audit
        if unpinned_actions:
            print(f"\n🔍 Security Audit: Found {len(unpinned_actions)} unpinned actions:")
            for item in unpinned_actions:
                print(f"  - {item['file']}: {item['action']} ({item['matches']})")
        
        # This test documents current state - it will fail until pinning is implemented
        self.assertEqual(len(unpinned_actions), 0, 
                        "Found unpinned GitHub Actions that should be pinned to commit SHAs")
    
    def test_validate_commit_sha_format(self):
        """Test validation of commit SHA format."""
        valid_shas = [
            "a1b2c3d4e5f6789012345678901234567890abcd",  # 40 chars
            "a1b2c3d4",  # short SHA
        ]
        
        invalid_shas = [
            "v4",  # version tag
            "main",  # branch name  
            "latest",  # tag name
            "123",  # too short
        ]
        
        sha_pattern = r'^[a-f0-9]{7,40}$'
        
        for sha in valid_shas:
            self.assertTrue(re.match(sha_pattern, sha), 
                           f"Valid SHA should match pattern: {sha}")
        
        for sha in invalid_shas:
            self.assertFalse(re.match(sha_pattern, sha),
                           f"Invalid SHA should not match pattern: {sha}")
    
    def test_security_principles(self):
        """Test adherence to security principles."""
        # Verify security audit file exists
        audit_file = Path(__file__).parent.parent / 'GITHUB_ACTIONS_SECURITY_AUDIT.md'
        self.assertTrue(audit_file.exists(), 
                       "Security audit documentation should exist")
        
        # Verify critical security actions are identified
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                content = f.read()
            
            critical_terms = ['trufflehog@main', 'CRITICAL', 'security']
            for term in critical_terms:
                self.assertIn(term, content,
                             f"Security audit should mention: {term}")


if __name__ == '__main__':
    unittest.main()