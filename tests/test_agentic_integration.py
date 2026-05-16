#!/usr/bin/env python3
"""
Unit tests for the agentic_integration module
Tests the AdaptiveAIEngineeringGovernanceSystem class
"""

import io
import unittest
import sys
import os
import json
from contextlib import redirect_stdout

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agentic_integration import AdaptiveAIEngineeringGovernanceSystem


class TestAdaptiveAIEngineeringGovernanceSystem(unittest.TestCase):
    """Unit tests for the Adaptive AI Engineering Governance System"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = AdaptiveAIEngineeringGovernanceSystem(verbose=False)

    def test_system_initialization(self):
        """Test that system initializes with all required components"""
        self.assertIsNotNone(self.system.config)
        self.assertIsNotNone(self.system.governance_orchestrator)
        self.assertIsNotNone(self.system.cost_engine)
        self.assertIsNotNone(self.system.reliability_framework)
        self.assertIsNotNone(self.system.human_collaboration)
        self.assertIsNotNone(self.system.compliance_engine)
        self.assertIsNotNone(self.system.metrics_engine)
        self.assertIsNotNone(self.system.developer_trust)

    def test_configuration_loading(self):
        """Test configuration loading with defaults"""
        config = self.system.config
        
        # Test required config sections exist
        self.assertIn('cost_budget', config)
        self.assertIn('reliability_targets', config)
        self.assertIn('compliance_frameworks', config)
        
        # Test default values
        self.assertEqual(config['cost_budget']['monthly_budget'], 1000.0)
        self.assertEqual(config['reliability_targets']['claude_build_slo'], 99.5)
        self.assertIn('SOX', config['compliance_frameworks'])

    def test_engineering_request_processing_simple(self):
        """Test processing a simple engineering request"""
        simple_request = {
            "type": "build",
            "component": "documentation",
            "description": "Update README with new examples", 
            "security_score": 1,
            "complexity": 2,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 10.0,
            "urgency": 1,
            "files_changed": ["README.md"],
            "technical_details": {"documentation_only": True}
        }

        result = self.system.process_engineering_request(
            request_type="build",
            repository="test-repo",
            change_request=simple_request,
            developer_id="test_developer"
        )

        # Verify result structure
        self.assertIn('governance_decision', result)
        self.assertIn('cognitive_summary', result)
        self.assertIn('compliance_evidence', result)
        self.assertIn('audit_trail', result)
        self.assertIn('metrics_summary', result)

        # Verify governance decision
        governance = result['governance_decision']
        self.assertIn('selected_agent', governance)
        self.assertIn('risk_assessment', governance)
        self.assertIn('confidence_score', governance)

    def test_engineering_request_processing_high_security(self):
        """Test processing a high-security engineering request"""
        security_request = {
            "type": "build",
            "component": "payment-processor",
            "description": "Implement PCI-compliant payment processing",
            "security_score": 10,
            "complexity": 8,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": True,
            "cost_budget": 100.0,
            "urgency": 4,
            "files_changed": ["payment/processor.py", "security/pci_compliance.py"],
            "technical_details": {
                "pci_compliance": True,
                "payment_processing": True,
                "fraud_detection": True
            }
        }

        result = self.system.process_engineering_request(
            request_type="build",
            repository="test-repo",
            change_request=security_request,
            developer_id="test_developer"
        )

        # High security should trigger specialized governance
        governance = result['governance_decision']
        self.assertGreaterEqual(governance['risk_assessment']['overall_risk_score'], 7)
        
        # Should have compliance evidence for regulated change
        self.assertGreater(len(result['compliance_evidence']), 0)

    def test_enterprise_dashboard_generation(self):
        """Test enterprise dashboard generation"""
        dashboard = self.system.generate_enterprise_dashboard()

        # Verify dashboard structure
        required_sections = [
            'system_status',
            'value_metrics', 
            'intelligence_status',
            'enterprise_capabilities',
            'unique_advantages'
        ]

        for section in required_sections:
            self.assertIn(section, dashboard)

        # Verify all 13 intelligence layers are represented
        intelligence_status = dashboard['intelligence_status']
        expected_layers = [
            'dynamic_agent_selection',
            'outcome_learning',
            'engineering_memory',
            'risk_intelligence',
            'explainability',
            'multi_repo_reasoning',
            'architecture_governance',
            'cost_awareness',
            'reliability_framework',
            'human_collaboration',
            'compliance_audit',
            'benchmarkable_metrics',
            'developer_trust'
        ]

        for layer in expected_layers:
            self.assertIn(layer, intelligence_status)

    def test_cost_optimization(self):
        """Test cost-aware optimization"""
        low_budget_request = {
            "type": "build",
            "component": "utility-helper",
            "description": "Add small utility function",
            "security_score": 2,
            "complexity": 3,
            "cost_budget": 3.0,  # Very tight budget
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "urgency": 1,
            "files_changed": ["utils/helpers.py"],
            "technical_details": {"utility_function": True}
        }

        result = self.system.process_engineering_request(
            request_type="build",
            repository="test-repo",
            change_request=low_budget_request,
            developer_id="test_developer"
        )

        # Should have cost optimization applied for tight budget
        governance = result['governance_decision']
        if 'cost_optimization' in governance:
            self.assertIn('original_agent', governance['cost_optimization'])
            self.assertIn('cost_optimized_agent', governance['cost_optimization'])

    def test_configuration_with_custom_file(self):
        """Test configuration loading with custom file"""
        # Create temporary config
        custom_config = {
            "cost_budget": {
                "monthly_budget": 2000.0,
                "cost_per_change_limit": 50.0
            },
            "developer_trust_mode": "strict"
        }
        
        config_path = "/tmp/test_config.json"
        with open(config_path, 'w') as f:
            json.dump(custom_config, f)
        
        try:
            system = AdaptiveAIEngineeringGovernanceSystem(config_path=config_path, verbose=False)
            
            # Custom values should be applied
            self.assertEqual(system.config['cost_budget']['monthly_budget'], 2000.0)
            self.assertEqual(system.config['cost_budget']['cost_per_change_limit'], 50.0)
            self.assertEqual(system.config['developer_trust_mode'], 'strict')
            
            # Defaults should still be present for unspecified values
            self.assertIn('compliance_frameworks', system.config)
            
        finally:
            if os.path.exists(config_path):
                os.remove(config_path)

    def test_error_handling(self):
        """Test error handling for invalid requests"""
        invalid_request = {
            "type": "invalid_type",
            "description": "This should handle gracefully"
        }

        # Should not crash on invalid request
        try:
            result = self.system.process_engineering_request(
                request_type="invalid",
                repository="test-repo", 
                change_request=invalid_request,
                developer_id="test_developer"
            )
            # Should return some result even with invalid input
            self.assertIsInstance(result, dict)
        except Exception as e:
            # If it does throw an exception, it should be informative
            self.assertIsInstance(e, (ValueError, KeyError, TypeError))

    def test_verbose_true_prints_output(self):
        """Test that verbose=True prints initialization output"""
        f = io.StringIO()
        with redirect_stdout(f):
            AdaptiveAIEngineeringGovernanceSystem(verbose=True)
        output = f.getvalue()
        self.assertIn("Adaptive AI Engineering Governance System initialized", output)

    def test_verbose_false_suppresses_output(self):
        """Test that verbose=False suppresses initialization output"""
        f = io.StringIO()
        with redirect_stdout(f):
            AdaptiveAIEngineeringGovernanceSystem(verbose=False)
        self.assertEqual(f.getvalue(), "")

    def test_verbose_suppressed_during_process_change(self):
        """Test that verbose=False suppresses phase output during request processing"""
        system = AdaptiveAIEngineeringGovernanceSystem(verbose=False)
        request = {
            "type": "build",
            "component": "documentation",
            "description": "Update README",
            "security_score": 1,
            "complexity": 2,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 10.0,
            "urgency": 1,
            "files_changed": ["README.md"],
            "technical_details": {}
        }
        f = io.StringIO()
        with redirect_stdout(f):
            system.process_engineering_request(
                request_type="build",
                repository="test-repo",
                change_request=request,
                developer_id="test_developer"
            )
        output = f.getvalue()
        self.assertNotIn("Phase 1", output)
        self.assertNotIn("Phase 4", output)
        self.assertNotIn("Phase 6", output)


if __name__ == '__main__':
    # Set up test environment
    print("Running unit tests for AdaptiveAIEngineeringGovernanceSystem...")
    
    # Run tests
    unittest.main(verbosity=2)