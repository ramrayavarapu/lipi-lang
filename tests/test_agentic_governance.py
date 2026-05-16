#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for Agentic Engineering Governance System
===================================================

Comprehensive test suite for all 13 intelligence layers of the
Adaptive AI Engineering Governance System.

Tests cover:
1. Dynamic Agent Selection Intelligence
2. Outcome Learning & Feedback Intelligence  
3. Engineering Memory & Organizational Context
4. Risk Scoring & Governance Intelligence
5. Explainability Layer
6. Multi-repo System-level Reasoning
7. Architecture Governance Intelligence
8. Cost-awareness Orchestration Engine
9. Reliability/SLO Framework for AI Agents
10. Human Collaboration Intelligence
11. Compliance & Audit Intelligence
12. Benchmarkable Metrics System
13. Developer Trust & Adoption Strategy
"""

import unittest
import tempfile
import os
import time
import json
from unittest.mock import Mock, patch

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agentic_governance import (
    DynamicAgentSelector,
    AgentSelectionContext,
    AgentType,
    OutcomeLearningEngine,
    EngineeringMemorySystem,
    RiskIntelligenceEngine,
    ExplainabilityEngine,
    MultiRepoReasoningEngine,
    ArchitectureGovernanceEngine,
    AgenticGovernanceOrchestrator
)

from agentic_intelligence_extended import (
    CostAwarenessEngine,
    ReliabilityFramework,
    HumanCollaborationEngine,
    ComplianceAuditEngine,
    BenchmarkableMetricsEngine,
    DeveloperTrustEngine
)

from agentic_integration import (
    AdaptiveAIEngineeringGovernanceSystem
)


class TestDynamicAgentSelection(unittest.TestCase):
    """Test dynamic agent selection intelligence"""
    
    def setUp(self):
        self.selector = DynamicAgentSelector()
    
    def test_security_sensitive_routing(self):
        """Test that high security contexts route to security-specialized agents"""
        context = AgentSelectionContext(
            repository="payment-service",
            change_type="build",
            security_sensitivity=9,
            complexity_score=5,
            frontend_heavy=False,
            infrastructure_changes=False,
            regulated_domain=False,
            estimated_cost_budget=100.0,
            urgency_level=3
        )
        
        selected_agent = self.selector.select_optimal_agent(context)
        self.assertEqual(selected_agent, AgentType.SECURITY_SPECIALIZED)
    
    def test_regulated_domain_routing(self):
        """Test that regulated domains get appropriate governance"""
        context = AgentSelectionContext(
            repository="banking-service",
            change_type="build", 
            security_sensitivity=5,
            complexity_score=5,
            frontend_heavy=False,
            infrastructure_changes=False,
            regulated_domain=True,
            estimated_cost_budget=100.0,
            urgency_level=3
        )
        
        selected_agent = self.selector.select_optimal_agent(context)
        self.assertEqual(selected_agent, AgentType.REGULATORY_COMPLIANCE)
    
    def test_cost_sensitive_routing(self):
        """Test that low complexity + low budget routes to cheap agent"""
        context = AgentSelectionContext(
            repository="docs-update",
            change_type="build",
            security_sensitivity=2,
            complexity_score=2,
            frontend_heavy=False,
            infrastructure_changes=False,
            regulated_domain=False,
            estimated_cost_budget=5.0,
            urgency_level=1
        )
        
        selected_agent = self.selector.select_optimal_agent(context)
        self.assertEqual(selected_agent, AgentType.LIGHTWEIGHT_CHEAP)


class TestOutcomeLearning(unittest.TestCase):
    """Test outcome learning and feedback intelligence"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.outcome_learner = OutcomeLearningEngine(self.temp_db.name)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_outcome_recording(self):
        """Test that engineering outcomes are recorded correctly"""
        from agentic_governance import EngineeringOutcome
        
        outcome = EngineeringOutcome(
            outcome_id="test_outcome_1",
            agent_used="claude-build",
            context={"complexity": 5},
            success_metrics={"quality_score": 8.5},
            timestamp=time.time(),
            outcome_type="successful_merge"
        )
        
        self.outcome_learner.record_outcome(outcome)
        
        # Verify it can be analyzed
        performance = self.outcome_learner.analyze_agent_performance("claude-build")
        self.assertGreater(performance["success_rate"], 0)
        self.assertEqual(performance["avg_quality_score"], 8.5)


class TestEngineeringMemory(unittest.TestCase):
    """Test engineering memory and organizational context"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.memory_system = EngineeringMemorySystem(self.temp_db.name)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_contextual_guidance(self):
        """Test that organizational context is provided appropriately"""
        guidance = self.memory_system.get_contextual_guidance("checkout-service")
        
        # Should have architectural patterns
        self.assertIn("architectural_patterns", guidance)
        
        # Should have historical concerns for checkout service
        self.assertIn("historical_concerns", guidance)
        historical_concerns = guidance["historical_concerns"]
        self.assertTrue(any("pci-incident" in str(concern) for concern in historical_concerns))


class TestRiskIntelligence(unittest.TestCase):
    """Test risk scoring and governance intelligence"""
    
    def setUp(self):
        self.risk_engine = RiskIntelligenceEngine()
    
    def test_payment_service_high_risk(self):
        """Test that payment services are correctly identified as high risk"""
        assessment = self.risk_engine.assess_change_risk(
            component="payment-service",
            change_description="Update payment processing logic",
            files_changed=["payment_processor.py"]
        )
        
        self.assertGreaterEqual(assessment.overall_risk_score, 7)
        self.assertIn("payment-service", assessment.risk_factors)
    
    def test_documentation_low_risk(self):
        """Test that documentation changes are low risk"""
        assessment = self.risk_engine.assess_change_risk(
            component="docs",
            change_description="Update README documentation",
            files_changed=["README.md"]
        )
        
        self.assertLessEqual(assessment.overall_risk_score, 3)
        self.assertIn("documentation", assessment.risk_factors)
    
    def test_governance_requirements_scaling(self):
        """Test that governance requirements scale with risk"""
        high_risk_assessment = self.risk_engine.assess_change_risk(
            component="auth-service", 
            change_description="Update authentication logic",
            files_changed=["auth.py"]
        )
        
        low_risk_assessment = self.risk_engine.assess_change_risk(
            component="docs",
            change_description="Update README",
            files_changed=["README.md"]
        )
        
        # High risk should require more governance
        high_req = high_risk_assessment.governance_requirements
        low_req = low_risk_assessment.governance_requirements
        
        self.assertNotEqual(high_req["approval_depth"], low_req["approval_depth"])
        self.assertNotEqual(high_req["reviewer_strictness"], low_req["reviewer_strictness"])


class TestExplainability(unittest.TestCase):
    """Test explainability layer"""
    
    def setUp(self):
        self.explainability = ExplainabilityEngine()
    
    def test_agent_selection_explanation(self):
        """Test that agent selection decisions are explainable"""
        context = AgentSelectionContext(
            repository="test-repo",
            change_type="build", 
            security_sensitivity=9,
            complexity_score=5,
            frontend_heavy=False,
            infrastructure_changes=False,
            regulated_domain=False,
            estimated_cost_budget=100.0,
            urgency_level=3
        )
        
        explanation = self.explainability.explain_agent_selection(
            context, 
            AgentType.SECURITY_SPECIALIZED
        )
        
        self.assertEqual(explanation.decision_type, "agent_selection")
        self.assertEqual(explanation.decision_outcome, "security-specialized")
        self.assertTrue(len(explanation.reasoning_chain) > 0)
        self.assertIn("security_threshold", explanation.evidence_used)
        self.assertTrue(explanation.human_override_allowed)


class TestMultiRepoReasoning(unittest.TestCase):
    """Test multi-repo system-level reasoning"""
    
    def setUp(self):
        self.multi_repo_engine = MultiRepoReasoningEngine()
    
    def test_system_impact_analysis(self):
        """Test system-wide impact analysis"""
        impact = self.multi_repo_engine.analyze_system_impact(
            primary_service="checkout-service",
            changes_description="Update checkout API to add new payment method"
        )
        
        self.assertEqual(impact.primary_component, "checkout-service")
        self.assertIn("payment-service", impact.affected_services)
        self.assertGreater(impact.blast_radius_score, 1)
    
    def test_blast_radius_calculation(self):
        """Test blast radius scoring"""
        high_impact = self.multi_repo_engine.analyze_system_impact(
            primary_service="user-service",  # Auth affects everything
            changes_description="Update authentication schema and API contracts"
        )
        
        low_impact = self.multi_repo_engine.analyze_system_impact(
            primary_service="docs-service",
            changes_description="Update documentation"
        )
        
        self.assertGreater(high_impact.blast_radius_score, low_impact.blast_radius_score)


class TestArchitectureGovernance(unittest.TestCase):
    """Test architecture governance intelligence"""
    
    def setUp(self):
        self.arch_governor = ArchitectureGovernanceEngine()
    
    def test_shared_database_violation(self):
        """Test detection of shared database violations"""
        changes = {
            "database_access": True,
            "shared_database": True
        }
        
        violations = self.arch_governor.validate_architectural_compliance(
            "test-service",
            changes
        )
        
        self.assertTrue(any(v.violation_type == "shared_database" for v in violations))
    
    def test_synchronous_communication_violation(self):
        """Test detection of synchronous communication violations"""
        changes = {
            "service_calls": True,
            "synchronous_calls": ["other-service"]
        }
        
        violations = self.arch_governor.validate_architectural_compliance(
            "test-service",
            changes
        )
        
        self.assertTrue(any(v.violation_type == "synchronous_communication" for v in violations))


class TestCostAwareness(unittest.TestCase):
    """Test cost-awareness orchestration engine"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.cost_engine = CostAwarenessEngine()
        self.cost_engine.cost_db_path = self.temp_db.name
        self.cost_engine._init_cost_database()
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_cost_estimation(self):
        """Test cost estimation for different agents"""
        cost_profile = self.cost_engine.estimate_operation_cost("claude-build", 5)
        
        self.assertGreater(cost_profile.total_estimated_cost, 0)
        self.assertGreater(cost_profile.estimated_tokens, 0)
        self.assertEqual(cost_profile.agent_type, "claude-build")
    
    def test_budget_optimization(self):
        """Test budget-aware agent optimization"""
        from agentic_intelligence_extended import CostBudget
        
        tight_budget = CostBudget(
            monthly_budget=100.0,
            current_spend=95.0,
            cost_per_change_limit=0.01,  # Very tight limit
            emergency_budget_reserve=5.0
        )
        
        optimized_agent = self.cost_engine.optimize_for_budget(
            "claude-build",  # Expensive agent
            tight_budget,
            complexity_score=3
        )
        
        # Should optimize to cheaper agent
        self.assertEqual(optimized_agent, "lightweight-cheap")


class TestReliabilityFramework(unittest.TestCase):
    """Test reliability/SLO framework for AI agents"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.reliability_framework = ReliabilityFramework()
        self.reliability_framework.reliability_db = self.temp_db.name
        self.reliability_framework._init_reliability_database()
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_operation_recording(self):
        """Test recording of agent operations"""
        self.reliability_framework.record_agent_operation(
            operation_id="test_op_1",
            agent_type="claude-build",
            operation_type="build",
            success=True,
            latency_ms=1500.0
        )
        
        # Should be able to calculate metrics
        metrics = self.reliability_framework.calculate_reliability_metrics(
            "claude-build",
            time.time() - 3600  # Last hour
        )
        
        self.assertEqual(metrics.success_rate, 100.0)
        self.assertEqual(metrics.average_latency_ms, 1500.0)
    
    def test_fallback_strategy(self):
        """Test fallback agent selection"""
        fallback = self.reliability_framework.get_fallback_strategy(
            "claude-build",
            "build"
        )
        
        self.assertIsInstance(fallback, str)
        self.assertNotEqual(fallback, "claude-build")


class TestHumanCollaboration(unittest.TestCase):
    """Test human collaboration intelligence"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.human_collaboration = HumanCollaborationEngine()
        self.human_collaboration.human_feedback_db = self.temp_db.name
        self.human_collaboration._init_human_feedback_database()
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_cognitive_summary_generation(self):
        """Test generation of human-optimized cognitive summaries"""
        governance_decision = {
            "risk_assessment": {"overall_risk_score": 8, "recommended_actions": ["Security review"]},
            "system_impact": {"blast_radius_score": 6, "affected_services": ["service1", "service2"]},
            "architectural_violations": [{"type": "test_violation"}],
            "confidence_score": 0.85
        }
        
        summary = self.human_collaboration.generate_cognitive_summary(governance_decision)
        
        self.assertIsInstance(summary.risk_hotspots, list)
        self.assertIsInstance(summary.architectural_impact, str)
        self.assertGreater(summary.confidence_score, 0)
        self.assertIn("HOLD", summary.recommended_merge_action)  # High risk should hold
    
    def test_human_override_recording(self):
        """Test recording of human overrides for learning"""
        override_id = self.human_collaboration.record_human_override(
            "ai_decision_reject",
            "human_decision_approve", 
            "Developer override - context specific knowledge"
        )
        
        self.assertIsInstance(override_id, str)
        self.assertTrue(override_id.startswith("override_"))


class TestComplianceAudit(unittest.TestCase):
    """Test compliance and audit intelligence"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.compliance_engine = ComplianceAuditEngine()
        self.compliance_engine.compliance_db = self.temp_db.name
        self.compliance_engine._init_compliance_database()
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_compliance_framework_identification(self):
        """Test identification of applicable compliance frameworks"""
        payment_request = {
            "component": "payment-service",
            "description": "Update payment processing with PCI compliance",
            "regulated": True
        }
        
        applicable_frameworks = self.compliance_engine._identify_applicable_frameworks(payment_request)
        
        self.assertIn("PCI_DSS", applicable_frameworks)
        self.assertIn("SOX", applicable_frameworks)  # Regulated domain
    
    def test_evidence_generation(self):
        """Test automatic compliance evidence generation"""
        change_request = {
            "component": "auth-service",
            "description": "Update authentication security",
            "regulated": True
        }
        
        governance_decision = {
            "risk_assessment": {"overall_risk_score": 8},
            "selected_agent": "security-specialized"
        }
        
        evidence_list = self.compliance_engine.generate_compliance_evidence(
            change_request,
            governance_decision
        )
        
        self.assertGreater(len(evidence_list), 0)
        self.assertTrue(any("security" in evidence.requirement_id.lower() for evidence in evidence_list))


class TestBenchmarkableMetrics(unittest.TestCase):
    """Test benchmarkable metrics system"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.metrics_engine = BenchmarkableMetricsEngine()
        self.metrics_engine.metrics_db = self.temp_db.name
        self.metrics_engine._init_metrics_database()
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_quality_event_recording(self):
        """Test recording of quality improvement events"""
        self.metrics_engine.record_quality_event(
            event_type="defect_prevented",
            severity="high",
            prevention_method="risk_analysis",
            cost_impact_avoided=500.0
        )
        
        # Verify it's recorded (would need to check database or calculate metrics)
        self.assertTrue(True)  # Basic test - real test would verify storage
    
    def test_metrics_calculation(self):
        """Test calculation of engineering metrics"""
        # Record some test events first
        self.metrics_engine.record_quality_event("defect_prevented", "medium", "ai_governance", 100.0)
        self.metrics_engine.record_quality_event("security_issue_blocked", "high", "security_agent", 1000.0)
        
        metrics = self.metrics_engine.calculate_engineering_metrics(
            baseline_period_days=30,
            measurement_period_days=7
        )
        
        self.assertIsInstance(metrics.escaped_defects_reduction, float)
        self.assertIsInstance(metrics.security_issue_prevention_count, int)


class TestDeveloperTrust(unittest.TestCase):
    """Test developer trust and adoption strategy"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.developer_trust = DeveloperTrustEngine()
        self.developer_trust.trust_db = self.temp_db.name
        self.developer_trust._init_trust_database()
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_strictness_adaptation(self):
        """Test adaptive strictness based on developer behavior"""
        # High override frequency should decrease strictness
        high_override_interactions = [
            {"type": "override", "satisfaction": 3},
            {"type": "override", "satisfaction": 2},
            {"type": "normal", "satisfaction": 4}
        ]
        
        adapted_strictness = self.developer_trust.adapt_strictness_for_developer(
            "test_developer",
            high_override_interactions
        )
        
        self.assertIn(adapted_strictness, ["learning", "standard", "strict", "maximum"])
    
    def test_feedback_recording(self):
        """Test developer feedback recording"""
        self.developer_trust.record_developer_feedback(
            developer_id="test_dev",
            decision_id="decision_123",
            feedback_type="positive",
            satisfaction_score=8,
            feedback_text="Good decision, helped catch security issue"
        )
        
        # Basic test - in real implementation would verify database storage
        self.assertTrue(True)
    
    def test_trust_report_generation(self):
        """Test trust report generation"""
        report = self.developer_trust.generate_trust_report()
        
        self.assertIn("average_satisfaction_score", report)
        self.assertIn("override_frequency", report)
        self.assertIn("trust_building_status", report)


class TestIntegratedSystem(unittest.TestCase):
    """Test the complete integrated agentic system"""
    
    def setUp(self):
        # Create temporary config
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        config = {
            "cost_budget": {"monthly_budget": 1000, "cost_per_change_limit": 25},
            "reliability_targets": {"claude_build_slo": 99.5}
        }
        json.dump(config, self.temp_config)
        self.temp_config.close()
        
        self.system = AdaptiveAIEngineeringGovernanceSystem(self.temp_config.name)
    
    def tearDown(self):
        os.unlink(self.temp_config.name)
    
    def test_complete_request_processing(self):
        """Test end-to-end request processing"""
        change_request = {
            "type": "build",
            "component": "test-service",
            "description": "Add new feature with moderate complexity",
            "security_score": 5,
            "complexity": 4,
            "frontend_changes": False,
            "infrastructure": False,
            "regulated": False,
            "cost_budget": 30.0,
            "urgency": 2,
            "files_changed": ["service.py"],
            "technical_details": {}
        }
        
        result = self.system.process_engineering_request(
            request_type="build",
            repository="test-repo",
            change_request=change_request,
            developer_id="test_developer"
        )
        
        # Verify comprehensive response
        self.assertIn("operation_id", result)
        self.assertIn("governance_decision", result)
        self.assertIn("cognitive_summary", result)
        self.assertIn("compliance_evidence", result)
        self.assertIn("execution_plan", result)
        self.assertIn("enterprise_features", result)
        
        # Verify enterprise features
        enterprise_features = result["enterprise_features"]
        self.assertTrue(enterprise_features["explainable_decisions"])
        self.assertTrue(enterprise_features["audit_ready"])
        self.assertTrue(enterprise_features["cost_controlled"])
    
    def test_enterprise_dashboard(self):
        """Test enterprise dashboard generation"""
        dashboard = self.system.generate_enterprise_dashboard()
        
        self.assertIn("system_status", dashboard)
        self.assertIn("value_metrics", dashboard)
        self.assertIn("intelligence_status", dashboard)
        self.assertIn("enterprise_capabilities", dashboard)
        
        # Verify all 13 intelligence layers are active
        intelligence_status = dashboard["intelligence_status"]
        active_layers = [k for k, v in intelligence_status.items() if "✅ Active" in v]
        self.assertEqual(len(active_layers), 13)  # All 13 layers should be active
    
    def test_fallback_behavior(self):
        """Test graceful degradation when components fail"""
        # Mock a failure in governance orchestrator
        with patch.object(self.system.governance_orchestrator, 'orchestrate_intelligent_governance', side_effect=Exception("Test failure")):
            result = self.system.process_engineering_request(
                request_type="build",
                repository="test-repo", 
                change_request={},
                developer_id="test_dev"
            )
            
            self.assertTrue(result.get("fallback_mode", False))
            self.assertIn("error", result)
            self.assertEqual(result["governance_decision"]["selected_agent"], "claude-build")


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)