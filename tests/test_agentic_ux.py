#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UX Tests for Agentic Engineering Governance System
=================================================

Tests key user flows and experience scenarios to ensure the system
provides value without becoming "AI bureaucracy". Tests the complete
user journey from design request to deployment governance.
"""

import unittest
import tempfile
import os
import json
import time

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agentic_integration import AdaptiveAIEngineeringGovernanceSystem


class TestDeveloperExperience(unittest.TestCase):
    """Test the developer user experience with the agentic system"""
    
    def setUp(self):
        self.system = AdaptiveAIEngineeringGovernanceSystem()
    
    def test_simple_documentation_change_flow(self):
        """Test that simple documentation changes have minimal friction"""
        # Scenario: Developer wants to update README with new features
        doc_change_request = {
            "type": "build",
            "component": "documentation",
            "description": "Update README with new Tamil language support",
            "security_score": 1,  # Very low security risk
            "complexity": 2,      # Simple change
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 15.0,
            "urgency": 1,
            "files_changed": ["README.md", "docs/TAMIL_GUIDE.md"],
            "technical_details": {
                "documentation_only": True,
                "no_code_changes": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="lipi-lang",
            change_request=doc_change_request,
            developer_id="doc_contributor"
        )
        
        # Should have minimal governance overhead
        governance_req = result["governance_decision"]["governance_requirements"]
        self.assertIn("automated", governance_req["approval_depth"].lower())
        self.assertEqual(governance_req["reviewer_strictness"], "minimal")
        
        # Should recommend quick approval
        merge_action = result["cognitive_summary"]["recommended_merge_action"]
        self.assertIn("APPROVE", merge_action)
        
        # Should have minimal human attention areas
        attention_areas = result["cognitive_summary"]["attention_required_areas"]
        self.assertLessEqual(len(attention_areas), 1)
        
        # Developer should not feel blocked
        self.assertNotIn("HOLD", merge_action)
        self.assertNotIn("security", merge_action.lower())
    
    def test_high_impact_security_change_flow(self):
        """Test that high-impact security changes get appropriate but not excessive governance"""
        # Scenario: Senior developer implementing critical security fix
        security_change_request = {
            "type": "build",
            "component": "auth-service",
            "description": "Fix critical authentication vulnerability in JWT validation",
            "security_score": 10,  # Critical security
            "complexity": 8,       # High complexity
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": True,
            "cost_budget": 100.0,
            "urgency": 5,         # Urgent fix needed
            "files_changed": ["auth/jwt_validator.py", "auth/security_policy.py"],
            "technical_details": {
                "security_critical": True,
                "auth_changes": True,
                "vulnerability_fix": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="auth-service",
            change_request=security_change_request,
            developer_id="senior_security_dev"
        )
        
        # Should route to security-specialized agent
        selected_agent = result["governance_decision"]["selected_agent"]
        self.assertEqual(selected_agent, "security-specialized")
        
        # Should require appropriate governance, but not excessive
        governance_req = result["governance_decision"]["governance_requirements"]
        self.assertIn("security", governance_req["approval_depth"].lower())
        self.assertEqual(governance_req["reviewer_strictness"], "maximum")
        
        # Should provide clear guidance on what's needed
        merge_action = result["cognitive_summary"]["recommended_merge_action"]
        self.assertIn("Security", merge_action)  # Should mention security review
        
        # Should have explainable reasoning
        explanations = result["governance_decision"]["agent_explanation"]
        self.assertGreater(len(explanations["reasoning_chain"]), 0)
        self.assertIn("security", " ".join(explanations["reasoning_chain"]).lower())
        
        # Should be urgent but controlled
        recommended_actions = result["governance_decision"]["recommended_actions"]
        self.assertTrue(any("security" in action.lower() for action in recommended_actions))
    
    def test_new_developer_onboarding_flow(self):
        """Test that new developers get supportive, educational experience"""
        # Scenario: New developer making their first contribution
        new_dev_request = {
            "type": "build",
            "component": "telugu-examples",
            "description": "Add new Telugu programming examples for beginners",
            "security_score": 2,
            "complexity": 3,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 20.0,
            "urgency": 2,
            "files_changed": ["examples/beginner_telugu.lipi.py"],
            "technical_details": {
                "examples_only": True,
                "educational_content": True
            }
        }
        
        # Simulate new developer with no interaction history (should get "learning" mode)
        result = self.system.process_engineering_request(
            request_type="build",
            repository="lipi-lang",
            change_request=new_dev_request,
            developer_id="new_contributor"
        )
        
        # Should adapt to supportive strictness level
        developer_adaptation = result["developer_adaptation"]
        self.assertIn(developer_adaptation["strictness_level"], ["learning", "standard"])
        
        # Should have reasonable governance (not too strict for learning)
        governance_req = result["governance_decision"]["governance_requirements"]
        self.assertNotEqual(governance_req["reviewer_strictness"], "maximum")
        
        # Should provide clear, educational feedback
        merge_action = result["cognitive_summary"]["recommended_merge_action"]
        self.assertIn(merge_action, ["APPROVE", "REVIEW"])  # Should not immediately block
        
        # Should have explainable decisions to help learning
        explanations = result["governance_decision"]["agent_explanation"]
        self.assertTrue(explanations["human_override_allowed"])
    
    def test_experienced_developer_efficiency_flow(self):
        """Test that experienced developers get efficient, streamlined experience"""
        # Scenario: Experienced developer with good track record making routine changes
        
        # First, simulate some positive interaction history by processing a few successful requests
        experienced_dev_id = "experienced_developer"
        
        routine_requests = [
            {
                "type": "build",
                "component": f"routine_feature_{i}",
                "description": f"Implement routine feature {i}",
                "security_score": 4,
                "complexity": 5,
                "frontend_changes": False,
                "infrastructure": False,
                "regulated": False,
                "cost_budget": 30.0,
                "urgency": 2,
                "files_changed": [f"feature_{i}.py"],
                "technical_details": {}
            }
            for i in range(2)
        ]
        
        # Process routine requests to build trust
        for request in routine_requests:
            self.system.process_engineering_request(
                request_type="build",
                repository="main-app",
                change_request=request,
                developer_id=experienced_dev_id
            )
        
        # Now test a more complex request
        complex_request = {
            "type": "build",
            "component": "performance-optimization",
            "description": "Optimize interpreter performance for large Telugu files", 
            "security_score": 3,
            "complexity": 7,  # More complex
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 60.0,
            "urgency": 3,
            "files_changed": ["src/lipi.py", "src/optimizer.py"],
            "technical_details": {
                "performance_optimization": True,
                "core_interpreter_changes": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="lipi-lang",
            change_request=complex_request,
            developer_id=experienced_dev_id
        )
        
        # Experienced developer should get reasonable governance
        governance_req = result["governance_decision"]["governance_requirements"]
        self.assertIn(governance_req["reviewer_strictness"], ["standard", "high"])  # Not maximum for trusted dev
        
        # Should still get appropriate oversight for complex change
        merge_action = result["cognitive_summary"]["recommended_merge_action"]
        self.assertIn(merge_action, ["APPROVE", "REVIEW"])
        
        # Should have efficiency optimizations
        if "cost_optimization" in result["governance_decision"]:
            cost_opt = result["governance_decision"]["cost_optimization"]
            self.assertIsNotNone(cost_opt)  # Some cost optimization should be present
    
    def test_multi_developer_collaboration_flow(self):
        """Test collaboration between multiple developers on the same project"""
        project_repo = "collaborative-project"
        
        # Developer 1: Frontend specialist working on UI
        frontend_request = {
            "type": "build",
            "component": "telugu-ui",
            "description": "Build Telugu language UI components",
            "security_score": 4,
            "complexity": 6,
            "frontend_changes": True,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 45.0,
            "urgency": 3,
            "files_changed": ["ui/telugu_components.js", "ui/language_selector.js"],
            "technical_details": {
                "ui_components": True,
                "internationalization": True
            }
        }
        
        frontend_result = self.system.process_engineering_request(
            request_type="build",
            repository=project_repo,
            change_request=frontend_request,
            developer_id="frontend_specialist"
        )
        
        # Should route to frontend-specialized agent
        self.assertEqual(frontend_result["governance_decision"]["selected_agent"], "frontend-specialized")
        
        # Developer 2: Backend specialist working on API
        backend_request = {
            "type": "build", 
            "component": "telugu-api",
            "description": "Build API endpoints for Telugu content processing",
            "security_score": 6,
            "complexity": 7,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 50.0,
            "urgency": 3,
            "files_changed": ["api/telugu_processor.py", "api/content_api.py"],
            "technical_details": {
                "api_endpoints": True,
                "text_processing": True
            }
        }
        
        backend_result = self.system.process_engineering_request(
            request_type="build",
            repository=project_repo,
            change_request=backend_request,
            developer_id="backend_specialist"
        )
        
        # Should route to appropriate agent (not frontend-specialized)
        self.assertNotEqual(backend_result["governance_decision"]["selected_agent"], "frontend-specialized")
        
        # Both should have appropriate system impact analysis
        self.assertIn("system_impact", frontend_result["governance_decision"])
        self.assertIn("system_impact", backend_result["governance_decision"])
        
        # Should consider multi-repo implications
        frontend_impact = frontend_result["governance_decision"]["system_impact"]
        backend_impact = backend_result["governance_decision"]["system_impact"]
        
        self.assertGreaterEqual(frontend_impact["blast_radius_score"], 1)
        self.assertGreaterEqual(backend_impact["blast_radius_score"], 1)
    
    def test_emergency_hotfix_flow(self):
        """Test that emergency hotfixes get expedited but safe processing"""
        # Scenario: Production bug needs immediate fix
        emergency_request = {
            "type": "build",
            "component": "critical-parser",
            "description": "Hotfix for Telugu character encoding bug causing interpreter crashes",
            "security_score": 6,  # Moderate security (interpreter vulnerability)
            "complexity": 4,      # Focused fix
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 75.0,  # Higher budget for urgency
            "urgency": 5,         # Maximum urgency
            "files_changed": ["src/telugu_parser.py"],
            "technical_details": {
                "production_bug": True,
                "interpreter_crash_fix": True,
                "character_encoding": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build", 
            repository="lipi-lang",
            change_request=emergency_request,
            developer_id="hotfix_developer"
        )
        
        # Should prioritize urgency but maintain safety
        merge_action = result["cognitive_summary"]["recommended_merge_action"]
        
        # Should not be blocked unless critical security issues
        if "HOLD" in merge_action:
            # If held, should have very good reason
            attention_areas = result["cognitive_summary"]["attention_required_areas"]
            self.assertTrue(any("security" in area.lower() or "critical" in area.lower() for area in attention_areas))
        else:
            # If not held, should be expedited
            self.assertIn(merge_action, ["APPROVE", "REVIEW"])
        
        # Should have clear guidance for fast resolution
        recommended_actions = result["governance_decision"]["recommended_actions"]
        self.assertGreater(len(recommended_actions), 0)
    
    def test_cost_conscious_organization_flow(self):
        """Test that cost-conscious organizations get appropriate optimizations"""
        # Scenario: Organization with tight AI budget needs cost optimization
        cost_conscious_request = {
            "type": "build",
            "component": "batch-processor",
            "description": "Process multiple Telugu files in batch mode",
            "security_score": 3,
            "complexity": 5,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 8.0,   # Very tight budget
            "urgency": 2,
            "files_changed": ["batch/processor.py", "batch/queue_manager.py"],
            "technical_details": {
                "batch_processing": True,
                "file_operations": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="cost-conscious-org",
            change_request=cost_conscious_request,
            developer_id="cost_conscious_dev"
        )
        
        # Should optimize for cost
        governance_decision = result["governance_decision"]
        
        # Should use cost-optimized agent
        if "cost_optimization" in governance_decision:
            cost_opt = governance_decision["cost_optimization"]
            self.assertEqual(cost_opt["cost_optimized_agent"], "lightweight-cheap")
        else:
            # If no explicit optimization, should still use appropriate agent
            selected_agent = governance_decision["selected_agent"]
            self.assertIn(selected_agent, ["lightweight-cheap", "copilot-review"])
        
        # Should still provide value despite cost constraints
        self.assertIn("governance_requirements", governance_decision)
        self.assertIn("cognitive_summary", result)
    
    def test_compliance_heavy_organization_flow(self):
        """Test that compliance-heavy organizations get appropriate governance"""
        # Scenario: Heavily regulated financial institution
        compliance_request = {
            "type": "build",
            "component": "financial-reporting",
            "description": "Generate Telugu financial reports with audit trail",
            "security_score": 8,
            "complexity": 7,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": True,
            "cost_budget": 120.0,
            "urgency": 3,
            "files_changed": ["reporting/financial_generator.py", "audit/trail_manager.py"],
            "technical_details": {
                "financial_data": True,
                "audit_requirements": True,
                "regulatory_reporting": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="financial-institution",
            change_request=compliance_request,
            developer_id="compliance_developer"
        )
        
        # Should route to compliance-aware agent
        selected_agent = result["governance_decision"]["selected_agent"]
        self.assertEqual(selected_agent, "regulatory-compliance")
        
        # Should generate comprehensive compliance evidence
        compliance_evidence = result["compliance_evidence"]
        self.assertGreater(len(compliance_evidence), 0)
        
        # Should have complete audit trail
        audit_trail = result["audit_trail"]
        self.assertIsNotNone(audit_trail["design_decision"])
        self.assertIsNotNone(audit_trail["code_implementation"])
        self.assertIsNotNone(audit_trail["review_evidence"])
        
        # Should require appropriate approvals
        governance_req = result["governance_decision"]["governance_requirements"]
        self.assertIn("senior", governance_req["approval_depth"].lower())
    
    def test_developer_override_and_learning_flow(self):
        """Test that developer overrides are handled gracefully and system learns"""
        # Scenario: Developer disagrees with AI recommendation and overrides
        override_request = {
            "type": "build",
            "component": "example-generator",
            "description": "Generate more Telugu programming examples",
            "security_score": 2,
            "complexity": 4,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 25.0,
            "urgency": 2,
            "files_changed": ["examples/advanced_telugu.py"],
            "technical_details": {
                "example_generation": True,
                "educational_content": True
            }
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="lipi-lang",
            change_request=override_request,
            developer_id="override_developer"
        )
        
        # Should allow human override
        agent_explanation = result["governance_decision"]["agent_explanation"]
        self.assertTrue(agent_explanation["human_override_allowed"])
        
        # Should have explainable reasoning that developer can understand
        reasoning = agent_explanation["reasoning_chain"]
        self.assertGreater(len(reasoning), 0)
        self.assertTrue(all(isinstance(reason, str) and len(reason) > 10 for reason in reasoning))
        
        # System should be prepared to learn from override
        # (In real system, human override would be recorded for learning)
        self.assertIn("enterprise_features", result)
        self.assertTrue(result["enterprise_features"]["explainable_decisions"])
    
    def test_dashboard_stakeholder_experience(self):
        """Test that stakeholders get valuable insights from enterprise dashboard"""
        # Generate dashboard as stakeholder would see it
        dashboard = self.system.generate_enterprise_dashboard()
        
        # Should have clear business value metrics
        value_metrics = dashboard["value_metrics"]
        
        # Should show ROI and improvements
        self.assertIn("cost_savings_monthly", value_metrics)
        self.assertIn("developer_productivity_improvement", value_metrics)
        self.assertIn("security_issues_prevented", value_metrics)
        
        # Should show system is working (not just busy)
        operational_metrics = dashboard["operational_metrics"]
        self.assertIn("total_ai_operations", operational_metrics)
        self.assertIn("developer_satisfaction", operational_metrics)
        
        # Should demonstrate uniqueness and competitive advantage
        unique_advantages = dashboard["unique_advantages"]
        self.assertGreater(len(unique_advantages), 5)  # Should have multiple advantages
        
        # Should show enterprise readiness
        enterprise_capabilities = dashboard["enterprise_capabilities"]
        self.assertIn("audit_trail_completeness", enterprise_capabilities)
        self.assertIn("compliance_automation", enterprise_capabilities)
        
        # All intelligence layers should be active
        intelligence_status = dashboard["intelligence_status"]
        active_layers = [k for k, v in intelligence_status.items() if "✅ Active" in v]
        self.assertEqual(len(active_layers), 13)  # All 13 layers active


if __name__ == "__main__":
    unittest.main(verbosity=2)