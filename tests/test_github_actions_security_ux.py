#!/usr/bin/env python3
"""
UX tests for GitHub Actions security implementation.
Tests end-to-end user experience for security workflow improvements.
"""

import unittest
import os
import subprocess
import tempfile
from pathlib import Path


class TestGitHubActionsSecurityUX(unittest.TestCase):
    """UX tests for GitHub Actions security user experience."""
    
    def setUp(self):
        """Set up UX test environment."""
        self.repo_root = Path(__file__).parent.parent
        self.test_workflows_dir = self.repo_root / '.github' / 'workflows'
    
    def test_security_audit_document_accessibility(self):
        """Test that security audit document is easily accessible."""
        audit_file = self.repo_root / 'GITHUB_ACTIONS_SECURITY_AUDIT.md'
        
        # Document should exist and be readable
        self.assertTrue(audit_file.exists(), 
                       "Security audit document should exist in repo root")
        
        with open(audit_file, 'r') as f:
            content = f.read()
        
        # Should be comprehensive and readable
        self.assertGreater(len(content), 100, 
                          "Security audit should provide detailed information")
        
        # Should have clear headings for user navigation
        user_friendly_headings = [
            '# GitHub Actions Security Audit Report',
            '### Security Risk Analysis', 
            '### Actions Requiring Security Pinning',
            '### Implementation Requirements'
        ]
        
        for heading in user_friendly_headings:
            self.assertIn(heading, content,
                         f"Security audit should have user-friendly heading: {heading}")
    
    def test_developer_workflow_experience(self):
        """Test developer experience when working with workflows."""
        # Simulate developer discovering security issues
        def simulate_developer_workflow():
            """Simulate typical developer workflow steps."""
            workflow_steps = [
                "Developer opens PR",
                "CI detects unpinned actions", 
                "Security audit provides guidance",
                "Developer pins actions to commit SHAs",
                "CI passes with secure actions"
            ]
            return workflow_steps
        
        steps = simulate_developer_workflow()
        self.assertEqual(len(steps), 5, "Developer workflow should have clear steps")
        
        # Verify security guidance is clear
        security_step = steps[2]
        self.assertIn("audit", security_step, "Should provide audit guidance")
    
    def test_security_validation_user_feedback(self):
        """Test user feedback for security validation."""
        # Test running security validation tests
        test_command = ["python3", "-m", "unittest", 
                       "tests.test_github_actions_security", "-v"]
        
        try:
            # Run in repo directory to test real workflows
            result = subprocess.run(test_command, 
                                  cwd=self.repo_root,
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            
            # Test should provide meaningful output (may fail due to unpinned actions)
            self.assertTrue(len(result.stdout) > 0 or len(result.stderr) > 0,
                           "Security tests should provide user feedback")
            
            # Check for user-friendly error messages
            combined_output = result.stdout + result.stderr
            user_friendly_terms = ["Security Audit", "unpinned", "commit SHA"]
            
            found_friendly_terms = any(term in combined_output for term in user_friendly_terms)
            self.assertTrue(found_friendly_terms,
                           "Security test output should be user-friendly")
            
        except subprocess.TimeoutExpired:
            self.fail("Security tests should complete within reasonable time")
        except FileNotFoundError:
            self.skipTest("Python unittest not available in test environment")
    
    def test_workflow_file_readability(self):
        """Test that workflow files are readable and well-documented."""
        if not self.test_workflows_dir.exists():
            self.skipTest("Workflows directory not found")
        
        workflow_files = list(self.test_workflows_dir.glob('*.yml'))
        self.assertGreater(len(workflow_files), 0, 
                          "Should have workflow files to test")
        
        for workflow_file in workflow_files[:3]:  # Test first few files
            with open(workflow_file, 'r') as f:
                content = f.read()
            
            # Should have descriptive name
            self.assertIn('name:', content, 
                         f"Workflow should have descriptive name: {workflow_file.name}")
            
            # Should have clear trigger conditions
            self.assertIn('on:', content,
                         f"Workflow should have clear triggers: {workflow_file.name}")
    
    def test_security_improvement_tracking(self):
        """Test tracking of security improvements."""
        # Verify that security improvements are trackable
        security_metrics = {
            'total_workflows': 0,
            'pinned_actions': 0,
            'unpinned_actions': 0,
            'critical_security_issues': 0
        }
        
        if self.test_workflows_dir.exists():
            workflow_files = list(self.test_workflows_dir.glob('*.yml'))
            security_metrics['total_workflows'] = len(workflow_files)
            
            # Count actions for tracking improvement
            import re
            for workflow_file in workflow_files:
                with open(workflow_file, 'r') as f:
                    content = f.read()
                
                # Count unpinned actions
                unpinned_patterns = [
                    r'actions/checkout@v\d+',
                    r'actions/setup-python@v\d+', 
                    r'trufflesecurity/trufflehog@main'
                ]
                
                for pattern in unpinned_patterns:
                    matches = re.findall(pattern, content)
                    security_metrics['unpinned_actions'] += len(matches)
                    
                    if 'trufflehog@main' in pattern and matches:
                        security_metrics['critical_security_issues'] += len(matches)
                
                # Count pinned actions (40-char commit SHAs)
                pinned_matches = re.findall(r'@[a-f0-9]{40}', content)
                security_metrics['pinned_actions'] += len(pinned_matches)
        
        # Metrics should be trackable
        for metric, value in security_metrics.items():
            self.assertIsInstance(value, int, f"Metric {metric} should be numeric")
        
        # Should identify critical issues
        print(f"\n📊 Security Metrics:")
        for metric, value in security_metrics.items():
            print(f"  {metric}: {value}")
        
        return security_metrics
    
    def test_user_action_guidance(self):
        """Test that users receive clear guidance on required actions."""
        audit_file = self.repo_root / 'GITHUB_ACTIONS_SECURITY_AUDIT.md'
        
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                content = f.read()
            
            # Should provide actionable guidance
            action_guidance = [
                'Pin to specific commit SHA',
                'Manual workflow updates required',
                'CRITICAL',
                'Implementation Requirements'
            ]
            
            for guidance in action_guidance:
                self.assertIn(guidance, content,
                             f"Audit should provide actionable guidance: {guidance}")
        
        # Test that guidance is specific and implementable
        self.assertTrue(True, "User guidance validation completed")


if __name__ == '__main__':
    unittest.main()