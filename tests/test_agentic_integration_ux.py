#!/usr/bin/env python3
"""
UX tests for the agentic_integration module
Tests end-to-end user experience flows and scenarios
"""

import unittest
import sys
import os
import json
import time
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agentic_integration import AdaptiveAIEngineeringGovernanceSystem


class TestAgenticIntegrationUX(unittest.TestCase):
    """UX tests for end-to-end user experience flows"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = AdaptiveAIEngineeringGovernanceSystem()

    def test_ux_new_developer_onboarding_flow(self):
        """Test UX flow for a new developer's first few changes"""
        # Scenario: New developer makes their first change
        new_developer_id = "new_dev_alice"
        
        # First change - simple documentation
        first_request = {
            "type": "build",
            "component": "documentation",
            "description": "Fix typo in README",
            "security_score": 1,
            "complexity": 1,
            "cost_budget": 2.0,
            "files_changed": ["README.md"]
        }

        result1 = self.system.process_engineering_request(
            request_type="build",
            repository="onboarding-repo",
            change_request=first_request,
            developer_id=new_developer_id
        )

        # Should provide good onboarding experience
        cognitive = result1['cognitive_summary']
        self.assertIn('recommended_merge_action', cognitive)
        
        # Should have clear explanations for new developer
        governance = result1['governance_decision']
        self.assertIn('agent_explanation', governance)
        
        # Second change - slightly more complex
        second_request = {
            "type": "build", 
            "component": "feature",
            "description": "Add new utility function",
            "security_score": 2,
            "complexity": 3,
            "cost_budget": 10.0,
            "files_changed": ["src/utils.py", "tests/test_utils.py"]
        }

        result2 = self.system.process_engineering_request(
            request_type="build",
            repository="onboarding-repo", 
            change_request=second_request,
            developer_id=new_developer_id
        )

        # System should adapt to developer's growing experience
        # (Developer trust should be building up)
        self.assertIsNotNone(result2['developer_trust_summary'])

    def test_ux_experienced_developer_efficiency_flow(self):
        """Test UX flow optimized for experienced developers"""
        experienced_dev_id = "senior_dev_bob"
        
        # Simulate experienced developer with good history
        # (In real system, this would come from historical data)
        complex_request = {
            "type": "build",
            "component": "core-engine",
            "description": "Refactor parser for better performance",
            "security_score": 4,
            "complexity": 6,
            "cost_budget": 40.0,
            "files_changed": [
                "src/parser.py",
                "src/optimizer.py", 
                "tests/test_parser.py"
            ],
            "technical_details": {
                "performance_optimization": True,
                "backward_compatible": True
            }
        }

        result = self.system.process_engineering_request(
            request_type="build",
            repository="main-repo",
            change_request=complex_request,
            developer_id=experienced_dev_id
        )

        # Should provide streamlined experience for experienced developer
        cognitive = result['cognitive_summary']
        
        # Should have appropriate level of governance (not overly bureaucratic)
        governance = result['governance_decision']
        approval_depth = governance['governance_requirements']['approval_depth']
        self.assertIn(approval_depth, ['automated-with-spot-check', 'peer-review'])  # Not overly strict

        # Should highlight what experienced dev needs to focus on
        attention_areas = cognitive['attention_required_areas']
        self.assertIsInstance(attention_areas, list)

    def test_ux_emergency_hotfix_flow(self):
        """Test UX flow for emergency hotfix scenarios"""
        hotfix_request = {
            "type": "build",
            "component": "security-patch",
            "description": "Critical security vulnerability fix",
            "security_score": 10,
            "complexity": 4,  # Fix is simple, but critical
            "cost_budget": 50.0,
            "urgency": 5,  # Maximum urgency
            "files_changed": ["src/security/validator.py"],
            "technical_details": {
                "security_critical": True,
                "hotfix": True,
                "production_issue": True
            }
        }

        result = self.system.process_engineering_request(
            request_type="build",
            repository="production-repo",
            change_request=hotfix_request,
            developer_id="oncall_dev"
        )

        # Should provide emergency-optimized experience
        governance = result['governance_decision']

        # Should have compliance evidence for security fix
        self.assertGreater(len(result['compliance_evidence']), 0)

        # Should provide clear action items for emergency
        cognitive = result['cognitive_summary']
        self.assertIn('recommended_merge_action', cognitive)

    def test_ux_cost_constrained_project_flow(self):
        """Test UX flow for cost-constrained projects"""
        low_budget_request = {
            "type": "build",
            "component": "enhancement",
            "description": "Add nice-to-have feature",
            "security_score": 2,
            "complexity": 5,
            "cost_budget": 5.0,  # Very tight budget
            "files_changed": ["src/features.py"],
            "technical_details": {"nice_to_have": True}
        }

        result = self.system.process_engineering_request(
            request_type="build",
            repository="budget-repo",
            change_request=low_budget_request,
            developer_id="budget_dev"
        )

        # Should provide cost-conscious UX
        governance = result['governance_decision']
        
        # Should suggest cost optimization
        if 'cost_optimization' in governance:
            cost_opt = governance['cost_optimization']
            self.assertIn('cost_optimized_agent', cost_opt)
        
        # Should return a complete response with cognitive summary
        cognitive = result['cognitive_summary']
        self.assertIn('recommended_merge_action', cognitive)

    def test_ux_compliance_heavy_project_flow(self):
        """Test UX flow for compliance-heavy regulated projects"""
        regulated_request = {
            "type": "build",
            "component": "financial-reporting",
            "description": "Update SOX compliance reporting module",
            "security_score": 8,
            "complexity": 7,
            "regulated": True,
            "cost_budget": 100.0,
            "files_changed": [
                "src/compliance/sox_reporting.py",
                "src/audit/trail_generator.py"
            ],
            "technical_details": {
                "sox_compliance": True,
                "audit_trail_required": True,
                "financial_impact": True
            }
        }

        result = self.system.process_engineering_request(
            request_type="build",
            repository="compliance-repo",
            change_request=regulated_request,
            developer_id="compliance_dev"
        )

        # Should provide compliance-focused UX
        governance = result['governance_decision']
        
        # Should require enhanced governance for compliance
        approval_depth = governance['governance_requirements']['approval_depth']
        self.assertIn(approval_depth, ['senior-developer-and-lead', 'senior-architect-and-security-team'])

        # Should generate comprehensive compliance evidence
        compliance_evidence = result['compliance_evidence']
        self.assertGreater(len(compliance_evidence), 0)

        # Should have detailed audit trail
        audit_trail = result['audit_trail']
        self.assertIn('approval_chain', audit_trail)

    def test_ux_multi_service_architecture_change_flow(self):
        """Test UX flow for changes affecting multiple services"""
        architecture_request = {
            "type": "build",
            "component": "user-authentication",
            "description": "Update auth system affecting all microservices",
            "security_score": 9,
            "complexity": 8,
            "infrastructure": True,
            "regulated": True,
            "cost_budget": 150.0,
            "files_changed": [
                "auth/core.py",
                "auth/jwt_handler.py",
                "api/middleware.py"
            ],
            "technical_details": {
                "affects_all_services": True,
                "api_contract_change": True,
                "breaking_change_potential": True
            }
        }

        result = self.system.process_engineering_request(
            request_type="build",
            repository="platform-repo",
            change_request=architecture_request,
            developer_id="architect_dev"
        )

        # Should provide system-wide impact analysis
        governance = result['governance_decision']
        
        # Should track system-wide impact
        system_impact = governance['system_impact']
        self.assertIn('affected_services', system_impact)

        # Should provide blast radius score
        self.assertIn('blast_radius_score', system_impact)
        
        # Should recommend thorough review for high-risk architecture changes
        cognitive = result['cognitive_summary']
        attention_areas = cognitive['attention_required_areas']
        self.assertIsInstance(attention_areas, list)

    def test_ux_dashboard_usability_flow(self):
        """Test UX flow for enterprise dashboard usability"""
        # Generate dashboard
        dashboard = self.system.generate_enterprise_dashboard()
        
        # Should be easy to understand at a glance
        self.assertIn('system_status', dashboard)
        status = dashboard['system_status']
        self.assertIsInstance(status, str)
        self.assertGreater(len(status), 0)

        # Value metrics should be business-friendly
        value_metrics = dashboard['value_metrics']
        expected_metrics = [
            'escaped_defects_reduction',
            'pr_review_time_reduction',
            'cost_savings_monthly',
            'security_issues_prevented'
        ]

        for metric in expected_metrics:
            self.assertIn(metric, value_metrics)

        # Intelligence status should be present for all layers
        intelligence_status = dashboard['intelligence_status']
        for layer, layer_status in intelligence_status.items():
            self.assertIsInstance(layer_status, str)
            self.assertGreater(len(layer_status), 0)
        
        # Should provide actionable insights
        self.assertIn('enterprise_capabilities', dashboard)
        self.assertIn('unique_advantages', dashboard)

    def test_ux_error_handling_and_recovery_flow(self):
        """Test UX flow for error handling and recovery"""
        # Simulate various error conditions
        error_scenarios = [
            # Incomplete request
            {"type": "build", "description": "Incomplete"},
            
            # Budget exceeded
            {
                "type": "build",
                "description": "Expensive change",
                "cost_budget": 10000.0,  # Way over budget
                "complexity": 10
            },
            
            # Conflicting requirements
            {
                "type": "build",
                "description": "Rush job with high security",
                "security_score": 10,
                "urgency": 5,
                "cost_budget": 1.0  # Impossible constraints
            }
        ]

        for i, error_scenario in enumerate(error_scenarios):
            try:
                result = self.system.process_engineering_request(
                    request_type="build",
                    repository="error-test-repo",
                    change_request=error_scenario,
                    developer_id=f"error_test_dev_{i}"
                )
                
                # If no exception, should provide helpful guidance
                if 'error_guidance' in result:
                    self.assertIn('recommendations', result['error_guidance'])
                    
            except Exception as e:
                # Should provide helpful error messages
                error_message = str(e)
                self.assertGreater(len(error_message), 10)  # Should be descriptive
                
                # Should suggest corrective actions
                self.assertTrue(
                    any(word in error_message.lower() 
                        for word in ['required', 'should', 'try', 'check'])
                )

    def test_ux_learning_and_adaptation_flow(self):
        """Test UX flow shows system learning and adaptation"""
        developer_id = "learning_test_dev"
        
        # Make similar requests to show adaptation
        base_request = {
            "type": "build",
            "component": "feature",
            "description": "Add new functionality",
            "security_score": 3,
            "complexity": 4,
            "cost_budget": 20.0
        }

        results = []
        for i in range(3):
            request = base_request.copy()
            request["description"] = f"Add new functionality - iteration {i+1}"
            request["files_changed"] = [f"src/feature_{i+1}.py"]
            
            result = self.system.process_engineering_request(
                request_type="build",
                repository="learning-repo",
                change_request=request,
                developer_id=developer_id
            )
            results.append(result)

        # Should show evidence of learning/adaptation in later results
        # (This is a simplified test - real system would have more sophisticated learning)
        
        # At minimum, should track developer interactions
        for result in results:
            self.assertIn('developer_trust_summary', result)


if __name__ == '__main__':
    print("Running UX tests for AdaptiveAIEngineeringGovernanceSystem...")
    unittest.main(verbosity=2)