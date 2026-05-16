#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Tests for Agentic Engineering Governance System
==================================================

Tests the API surface and integration points of the Agentic System.
Validates behavior at the system boundaries and interfaces.
"""

import unittest
import tempfile
import os
import json
import time
from unittest.mock import Mock, patch

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agentic_integration import AdaptiveAIEngineeringGovernanceSystem


class TestAgenticSystemAPI(unittest.TestCase):
    """Test the main API interface of the agentic system"""
    
    def setUp(self):
        self.system = AdaptiveAIEngineeringGovernanceSystem()
    
    def test_process_design_request(self):
        """Test processing design-type requests"""
        change_request = {
            "type": "design",
            "component": "new-service",
            "description": "Design a new microservice for user analytics",
            "security_score": 6,
            "complexity": 7,
            "frontend_changes": False,
            "infrastructure": True,
            "regulated": False,
            "cost_budget": 50.0,
            "urgency": 3,
            "files_changed": [],
            "technical_details": {
                "new_service": True,
                "database_required": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="design",
            repository="analytics-platform",
            change_request=change_request,
            developer_id="design_agent"
        )
        
        # Validate API response structure
        self.assertIn("operation_id", result)
        self.assertIn("governance_decision", result)
        self.assertIn("execution_plan", result)
        
        # Validate design-specific routing
        selected_agent = result["governance_decision"]["selected_agent"]
        self.assertIn("chatgpt", selected_agent.lower().replace("_", "-").replace("-", ""))  # Design should route to design agent
    
    def test_process_build_request(self):
        """Test processing build-type requests"""
        change_request = {
            "type": "build",
            "component": "payment-processor",
            "description": "Implement payment processing with fraud detection",
            "security_score": 9,
            "complexity": 8,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": True,
            "cost_budget": 75.0,
            "urgency": 4,
            "files_changed": ["payment.py", "fraud_detection.py"],
            "technical_details": {
                "database_access": True,
                "external_apis": ["fraud_service", "payment_gateway"],
                "pii_handling": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="payment-service",
            change_request=change_request,
            developer_id="build_agent"
        )
        
        # High security + regulated should route appropriately
        selected_agent = result["governance_decision"]["selected_agent"]
        
        # Should be either security-specialized or regulatory-compliance
        self.assertIn(selected_agent, ["security-specialized", "regulatory-compliance"])
        
        # High risk should require strict governance
        governance_req = result["governance_decision"]["governance_requirements"]
        self.assertIn("senior", governance_req.get("approval_depth", "").lower())
    
    def test_process_review_request(self):
        """Test processing review-type requests"""
        change_request = {
            "type": "review",
            "component": "documentation",
            "description": "Review documentation updates for API changes",
            "security_score": 2,
            "complexity": 3,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 10.0,
            "urgency": 1,
            "files_changed": ["API_DOCS.md", "README.md"],
            "technical_details": {
                "documentation_only": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="review",
            repository="docs",
            change_request=change_request,
            developer_id="reviewer"
        )
        
        # Low risk documentation should get minimal governance
        governance_req = result["governance_decision"]["governance_requirements"]
        self.assertIn("automated", governance_req.get("approval_depth", "").lower())
        
        # Should suggest quick approval
        merge_rec = result["cognitive_summary"]["recommended_merge_action"]
        self.assertIn("APPROVE", merge_rec)
    
    def test_cost_budget_enforcement(self):
        """Test that cost budgets are enforced correctly"""
        expensive_change_request = {
            "type": "build",
            "component": "complex-ai-service",
            "description": "Build complex AI processing service with multiple models",
            "security_score": 7,
            "complexity": 10,  # Very complex
            "frontend_changes": True,
            "infrastructure": True,
            "regulated": True,
            "cost_budget": 5.0,  # Very tight budget
            "urgency": 5,
            "files_changed": ["ai_model.py", "training.py", "inference.py"],
            "technical_details": {
                "ai_models_required": True,
                "gpu_processing": True,
                "large_datasets": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="ai-platform",
            change_request=expensive_change_request,
            developer_id="ai_developer"
        )
        
        # Should have cost optimization applied
        if "cost_optimization" in result["governance_decision"]:
            cost_opt = result["governance_decision"]["cost_optimization"]
            self.assertIn("cost_optimized_agent", cost_opt)
            # Should optimize to cheaper agent
            self.assertEqual(cost_opt["cost_optimized_agent"], "lightweight-cheap")
    
    def test_reliability_fallback(self):
        """Test reliability fallback behavior"""
        # Mock a failing agent
        with patch.object(self.system.reliability_framework, 'calculate_reliability_metrics') as mock_metrics:
            # Mock low availability
            mock_metrics.return_value = Mock(availability=95.0)  # Below SLO threshold
            
            change_request = {
                "type": "build",
                "component": "test-service",
                "description": "Test reliability fallback",
                "security_score": 5,
                "complexity": 5,
                "cost_budget": 50.0,
                "urgency": 3,
                "files_changed": ["test.py"],
                "technical_details": {}
            }
            
            result = self.system.process_engineering_request(
                request_type="build",
                repository="test-repo",
                change_request=change_request,
                developer_id="test_dev"
            )
            
            # Should have reliability fallback information
            if "reliability_fallback" in result["governance_decision"]:
                fallback = result["governance_decision"]["reliability_fallback"]
                self.assertIn("fallback_agent", fallback)
                self.assertIn("reason", fallback)
    
    def test_multi_framework_compliance(self):
        """Test compliance with multiple regulatory frameworks"""
        healthcare_payment_request = {
            "type": "build",
            "component": "healthcare-payment-service", 
            "description": "Process healthcare payments with patient data",
            "security_score": 10,
            "complexity": 8,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": True,
            "cost_budget": 100.0,
            "urgency": 4,
            "files_changed": ["patient_billing.py", "hipaa_compliance.py"],
            "technical_details": {
                "patient_data": True,
                "payment_processing": True,
                "phi_handling": True,
                "pci_required": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="healthcare-billing",
            change_request=healthcare_payment_request,
            developer_id="healthcare_dev"
        )
        
        # Should generate evidence for multiple frameworks
        compliance_evidence = result["compliance_evidence"]
        framework_types = {evidence["requirement_id"].split("_")[0] for evidence in compliance_evidence}
        
        # Should cover multiple compliance frameworks
        self.assertGreater(len(framework_types), 1)
        
        # Should include healthcare and payment frameworks
        self.assertTrue(
            any(framework in ["HIPAA", "PCI", "SOX"] for framework in framework_types)
        )


class TestAgenticSystemIntegration(unittest.TestCase):
    """Test integration with existing lipi-lang system"""
    
    def setUp(self):
        self.system = AdaptiveAIEngineeringGovernanceSystem()
    
    def test_lipi_lang_enhancement_integration(self):
        """Test that agentic system enhances lipi-lang appropriately"""
        lipi_enhancement_request = {
            "type": "build",
            "component": "lipi-interpreter",
            "description": "Add new Telugu language features to lipi interpreter",
            "security_score": 4,  # Language interpreter - moderate security
            "complexity": 6,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 40.0,
            "urgency": 3,
            "files_changed": ["src/lipi.py", "src/telugu_parser.py"],
            "technical_details": {
                "language_features": True,
                "parser_updates": True,
                "interpreter_core": True
            },
            "requirement_source": "design_issue_64"
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="lipi-lang",
            change_request=lipi_enhancement_request,
            developer_id="lipi_developer"
        )
        
        # Should process successfully with appropriate governance
        self.assertEqual(result["repository"], "lipi-lang")
        self.assertIn("lipi-interpreter", result["governance_decision"]["risk_assessment"]["risk_factors"])
        
        # Should have reasonable governance for moderate complexity change
        merge_action = result["cognitive_summary"]["recommended_merge_action"]
        self.assertIn(merge_action, ["APPROVE", "REVIEW"])  # Should not be HOLD for moderate risk
    
    def test_standards_md_workflow_enhancement(self):
        """Test that the system enhances the STANDARDS.md workflow"""
        # Test that all phases of STANDARDS.md are enhanced
        
        # Rule 1: Design - should have organizational memory
        design_request = {
            "type": "design", 
            "component": "new-feature",
            "description": "Design new bilingual feature",
            "cost_budget": 30.0,
            "files_changed": []
        }
        
        design_result = self.system.process_engineering_request("design", "lipi-lang", design_request)
        self.assertIn("governance_decision", design_result)
        
        # Rule 2: Build - should have risk-aware agent selection
        build_request = {
            "type": "build",
            "component": "security-feature", 
            "description": "Implement security validation",
            "security_score": 8,
            "cost_budget": 50.0,
            "files_changed": ["security.py"]
        }
        
        build_result = self.system.process_engineering_request("build", "lipi-lang", build_request)
        selected_agent = build_result["governance_decision"]["selected_agent"]
        self.assertEqual(selected_agent, "security-specialized")  # High security should route to security agent
        
        # Rule 3: Review - should have multi-repo reasoning
        review_request = {
            "type": "review",
            "component": "api-changes",
            "description": "Review API contract changes",
            "cost_budget": 20.0,
            "files_changed": ["api.py"]
        }
        
        review_result = self.system.process_engineering_request("review", "lipi-lang", review_request)
        self.assertIn("system_impact", review_result["governance_decision"])
        
        # Rule 4: Human - should have collaboration intelligence
        self.assertIn("cognitive_summary", review_result)
        self.assertIsInstance(review_result["cognitive_summary"]["risk_hotspots"], list)
    
    def test_enterprise_dashboard_api(self):
        """Test enterprise dashboard API"""
        dashboard = self.system.generate_enterprise_dashboard()
        
        # Validate dashboard structure
        required_sections = [
            "system_status",
            "value_metrics", 
            "operational_metrics",
            "intelligence_status",
            "enterprise_capabilities",
            "unique_advantages",
            "advanced_features"
        ]
        
        for section in required_sections:
            self.assertIn(section, dashboard)
        
        # Validate that all 13 intelligence layers are reported
        intelligence_status = dashboard["intelligence_status"]
        self.assertEqual(len(intelligence_status), 13)
        
        # All should be active
        active_count = sum(1 for status in intelligence_status.values() if "✅ Active" in status)
        self.assertEqual(active_count, 13)
    
    def test_error_handling_and_graceful_degradation(self):
        """Test error handling and graceful degradation"""
        # Test with malformed request
        malformed_request = {
            # Missing required fields
            "description": "Test malformed request"
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="test-repo",
            change_request=malformed_request,
            developer_id="test_dev"
        )
        
        # Should not crash, should provide fallback
        self.assertIn("operation_id", result)
        
        # If fallback mode, should indicate it
        if result.get("fallback_mode"):
            self.assertIn("error", result)
            self.assertEqual(result["governance_decision"]["selected_agent"], "claude-build")  # Safe default
    
    def test_developer_trust_adaptation_api(self):
        """Test developer trust adaptation through API"""
        # Simulate multiple requests from same developer
        developer_id = "adaptive_developer"
        
        requests = [
            {
                "type": "build",
                "component": f"feature_{i}",
                "description": f"Build feature {i}",
                "security_score": 5,
                "complexity": 4,
                "cost_budget": 25.0,
                "urgency": 2,
                "files_changed": [f"feature_{i}.py"],
                "technical_details": {}
            }
            for i in range(3)
        ]
        
        results = []
        for i, request in enumerate(requests):
            result = self.system.process_engineering_request(
                request_type="build",
                repository="test-adaptation",
                change_request=request,
                developer_id=developer_id
            )
            results.append(result)
        
        # Should have developer adaptation information
        for result in results:
            self.assertIn("developer_adaptation", result)
            adaptation = result["developer_adaptation"]
            self.assertIn("strictness_level", adaptation)
            self.assertIn(adaptation["strictness_level"], ["learning", "standard", "strict", "maximum"])


class TestAgenticSystemPerformance(unittest.TestCase):
    """Test performance characteristics of the agentic system"""
    
    def setUp(self):
        self.system = AdaptiveAIEngineeringGovernanceSystem()
    
    def test_response_time_performance(self):
        """Test that system responds within reasonable time limits"""
        start_time = time.time()
        
        change_request = {
            "type": "build",
            "component": "performance-test",
            "description": "Test system performance",
            "security_score": 5,
            "complexity": 5,
            "cost_budget": 30.0,
            "urgency": 3,
            "files_changed": ["test.py"],
            "technical_details": {}
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="performance-test",
            change_request=change_request,
            developer_id="perf_tester"
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete within reasonable time (adjust threshold as needed)
        self.assertLess(processing_time, 10.0, "System should respond within 10 seconds")
        
        # Should have all required components
        self.assertIn("operation_id", result)
        self.assertIn("governance_decision", result)
    
    def test_concurrent_request_handling(self):
        """Test handling of multiple concurrent requests"""
        # Note: This is a simplified test - real concurrency testing would use threading
        
        requests = [
            {
                "type": "build",
                "component": f"concurrent_test_{i}",
                "description": f"Concurrent test {i}",
                "security_score": 3 + i,
                "complexity": 4,
                "cost_budget": 20.0,
                "urgency": 2,
                "files_changed": [f"test_{i}.py"],
                "technical_details": {}
            }
            for i in range(5)
        ]
        
        results = []
        for i, request in enumerate(requests):
            result = self.system.process_engineering_request(
                request_type="build",
                repository=f"concurrent_repo_{i}",
                change_request=request,
                developer_id=f"concurrent_dev_{i}"
            )
            results.append(result)
        
        # All requests should complete successfully
        self.assertEqual(len(results), 5)
        
        # Each should have unique operation IDs
        operation_ids = [result["operation_id"] for result in results]
        self.assertEqual(len(set(operation_ids)), 5)  # All unique
        
        # All should have valid governance decisions
        for result in results:
            self.assertIn("governance_decision", result)
            self.assertIn("selected_agent", result["governance_decision"])


if __name__ == "__main__":
    unittest.main(verbosity=2)