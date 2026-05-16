#!/usr/bin/env python3
"""
API tests for the agentic_integration module
Tests the end-to-end API behavior and integration points
"""

import unittest
import sys
import os
import json
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agentic_integration import AdaptiveAIEngineeringGovernanceSystem


class TestAgenticIntegrationAPI(unittest.TestCase):
    """API tests for the Agentic Integration system"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = AdaptiveAIEngineeringGovernanceSystem(verbose=False)
        self.test_repository = "lipi-lang-test"

    def test_full_api_workflow_documentation_change(self):
        """Test complete API workflow for a documentation change"""
        request = {
            "type": "build",
            "component": "documentation",
            "description": "Add Telugu programming examples to README",
            "security_score": 1,
            "complexity": 2,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 10.0,
            "urgency": 1,
            "files_changed": ["README.md", "docs/telugu_examples.md"],
            "technical_details": {"documentation_only": True}
        }

        # Process the request
        start_time = time.time()
        result = self.system.process_engineering_request(
            request_type="build",
            repository=self.test_repository,
            change_request=request,
            developer_id="api_test_dev"
        )
        end_time = time.time()

        # API response time should be reasonable (< 5 seconds for this simple request)
        self.assertLess(end_time - start_time, 5.0)

        # Validate complete API response structure
        self._validate_api_response_structure(result)

        # For documentation change, expect minimal governance
        governance = result['governance_decision']
        self.assertLessEqual(governance['risk_assessment']['overall_risk_score'], 3)
        
        # Should have lightweight approval process
        self.assertEqual(governance['governance_requirements']['approval_depth'], 'automated-with-spot-check')

    def test_full_api_workflow_security_change(self):
        """Test complete API workflow for a security-sensitive change"""
        request = {
            "type": "build",
            "component": "authentication-system",
            "description": "Update JWT token validation with new security standards",
            "security_score": 9,
            "complexity": 7,
            "frontend_changes": True,
            "infrastructure": True,
            "regulated": True,
            "cost_budget": 75.0,
            "urgency": 3,
            "files_changed": [
                "auth/jwt_handler.py",
                "auth/security_validation.py",
                "frontend/auth_components.js"
            ],
            "technical_details": {
                "security_critical": True,
                "auth_protocol_change": True,
                "affects_all_services": True
            }
        }

        # Process the security request
        result = self.system.process_engineering_request(
            request_type="build",
            repository=self.test_repository,
            change_request=request,
            developer_id="security_test_dev"
        )

        # Validate API response
        self._validate_api_response_structure(result)

        # Security change should trigger high governance
        governance = result['governance_decision']
        self.assertGreaterEqual(governance['risk_assessment']['overall_risk_score'], 7)
        
        # Should require enhanced approval
        self.assertIn(governance['governance_requirements']['approval_depth'],
                      ['senior-architect-and-security-team', 'senior-developer-and-lead'])

        # Should have compliance evidence
        self.assertGreater(len(result['compliance_evidence']), 0)

        # Should track multi-service impact
        self.assertIn('affected_services', governance['system_impact'])

    def test_api_batch_request_processing(self):
        """Test processing multiple requests in batch"""
        requests = [
            {
                "id": "req_1",
                "request": {
                    "type": "build",
                    "component": "utility",
                    "description": "Add helper function",
                    "security_score": 1,
                    "complexity": 2,
                    "cost_budget": 5.0,
                    "files_changed": ["utils/helpers.py"]
                }
            },
            {
                "id": "req_2", 
                "request": {
                    "type": "build",
                    "component": "database",
                    "description": "Update database schema", 
                    "security_score": 6,
                    "complexity": 5,
                    "cost_budget": 30.0,
                    "infrastructure": True,
                    "files_changed": ["db/migrations/001_update_schema.sql"]
                }
            }
        ]

        results = []
        for req in requests:
            result = self.system.process_engineering_request(
                request_type="build",
                repository=self.test_repository,
                change_request=req["request"],
                developer_id=f"batch_test_{req['id']}"
            )
            result['request_id'] = req['id']
            results.append(result)

        # All requests should be processed successfully
        self.assertEqual(len(results), 2)
        
        # Each should have proper API structure
        for result in results:
            self._validate_api_response_structure(result)
            self.assertIn('request_id', result)

        # Results should select different agents based on request characteristics
        agents = [r['governance_decision']['selected_agent'] for r in results]
        self.assertNotEqual(agents[0], agents[1])

    def test_api_dashboard_endpoint(self):
        """Test enterprise dashboard API endpoint"""
        dashboard = self.system.generate_enterprise_dashboard()

        # Should be valid JSON-serializable
        json_str = json.dumps(dashboard)
        parsed_dashboard = json.loads(json_str)
        self.assertEqual(dashboard, parsed_dashboard)

        # Should have consistent API structure
        required_top_level_keys = [
            'system_status',
            'value_metrics',
            'intelligence_status', 
            'enterprise_capabilities',
            'unique_advantages'
        ]

        for key in required_top_level_keys:
            self.assertIn(key, dashboard)
            self.assertIsNotNone(dashboard[key])

        # Value metrics should have expected keys and numeric reduction/percentage values
        value_metrics = dashboard['value_metrics']
        self.assertIn('escaped_defects_reduction', value_metrics)
        self.assertIn('pr_review_time_reduction', value_metrics)
        for metric_name, metric_value in value_metrics.items():
            if 'reduction' in metric_name.lower():
                self.assertIsInstance(metric_value, (int, float))

    def test_api_error_responses(self):
        """Test API error handling and response formats"""
        error_cases = [
            # Missing required fields
            {"type": "build"},
            
            # Invalid types
            {"type": "invalid_type", "description": "test"},
            
            # Malformed data
            {"type": "build", "security_score": "not_a_number"},
        ]

        for error_case in error_cases:
            try:
                result = self.system.process_engineering_request(
                    request_type="build",
                    repository=self.test_repository,
                    change_request=error_case,
                    developer_id="error_test_dev"
                )
                
                # If no exception, should still return valid structure
                self.assertIsInstance(result, dict)
                
            except Exception as e:
                # Should be informative exceptions
                self.assertIsInstance(e, (ValueError, KeyError, TypeError))
                self.assertTrue(len(str(e)) > 0)

    def test_api_performance_requirements(self):
        """Test API meets performance requirements"""
        simple_request = {
            "type": "build",
            "component": "test",
            "description": "Simple test change",
            "security_score": 1,
            "complexity": 1,
            "cost_budget": 5.0
        }

        # Measure processing time
        start_time = time.time()
        result = self.system.process_engineering_request(
            request_type="build",
            repository=self.test_repository,
            change_request=simple_request,
            developer_id="perf_test_dev"
        )
        end_time = time.time()

        processing_time = end_time - start_time
        
        # Simple requests should process quickly (< 2 seconds)
        self.assertLess(processing_time, 2.0)
        
        # Should still return complete response
        self._validate_api_response_structure(result)

    def test_api_consistency_across_calls(self):
        """Test API returns consistent results for identical requests"""
        request = {
            "type": "build",
            "component": "consistency-test",
            "description": "Test consistency",
            "security_score": 3,
            "complexity": 3,
            "cost_budget": 15.0,
            "files_changed": ["test/consistency.py"]
        }

        # Make same request multiple times
        results = []
        for i in range(3):
            result = self.system.process_engineering_request(
                request_type="build",
                repository=self.test_repository,
                change_request=request,
                developer_id="consistency_test_dev"
            )
            results.append(result)

        # Key governance decisions should be consistent
        agents = [r['governance_decision']['selected_agent'] for r in results]
        risk_scores = [r['governance_decision']['risk_assessment']['overall_risk_score'] for r in results]
        
        # Should be same agent selection (allowing for minor variations in risk calculation)
        self.assertTrue(len(set(agents)) <= 2)  # Allow for minimal variation
        
        # Risk scores should be very similar
        max_risk_diff = max(risk_scores) - min(risk_scores)
        self.assertLessEqual(max_risk_diff, 1.0)

    def _validate_api_response_structure(self, result):
        """Helper to validate standard API response structure"""
        required_keys = [
            'governance_decision',
            'cognitive_summary', 
            'compliance_evidence',
            'audit_trail',
            'metrics_summary'
        ]

        for key in required_keys:
            self.assertIn(key, result, f"Missing required key: {key}")
            self.assertIsNotNone(result[key], f"Key {key} should not be None")

        # Validate governance decision structure
        governance = result['governance_decision']
        governance_required_keys = ['selected_agent', 'risk_assessment', 'confidence_score']
        for key in governance_required_keys:
            self.assertIn(key, governance, f"Missing governance key: {key}")

        # Validate risk assessment structure
        risk_assessment = governance['risk_assessment']
        self.assertIn('overall_risk_score', risk_assessment)
        self.assertIsInstance(risk_assessment['overall_risk_score'], (int, float))
        self.assertGreaterEqual(risk_assessment['overall_risk_score'], 0)
        self.assertLessEqual(risk_assessment['overall_risk_score'], 10)


if __name__ == '__main__':
    print("Running API tests for AdaptiveAIEngineeringGovernanceSystem...")
    unittest.main(verbosity=2)
