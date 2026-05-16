#!/usr/bin/env python3
"""
Unit tests for the Dynamic Agent Selection Intelligence Layer

Tests cover:
- Task classification accuracy
- Agent selection decision-making logic  
- Outcome learning and adaptation
- Edge cases and error handling
- Performance metrics calculation
"""

import unittest
import tempfile
import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from src.agent_intelligence import (
    RoutingIntelligenceLayer, TaskContext, AgentCapability, OutcomeRecord,
    TaskType, SecurityLevel, ComplexityLevel, AgentType,
    classify_task, get_routing_intelligence
)


class TestTaskClassification(unittest.TestCase):
    """Test task classification logic"""
    
    def test_design_task_classification(self):
        """Test design task classification"""
        task_type, security, complexity = classify_task("Design user authentication system")
        self.assertEqual(task_type, TaskType.DESIGN)
        
        task_type, security, complexity = classify_task("Plan database architecture")
        self.assertEqual(task_type, TaskType.DESIGN)
        
        task_type, security, complexity = classify_task("Create specification for API")
        self.assertEqual(task_type, TaskType.DESIGN)
    
    def test_build_task_classification(self):
        """Test build task classification"""
        task_type, security, complexity = classify_task("Implement user registration")
        self.assertEqual(task_type, TaskType.BUILD)
        
        task_type, security, complexity = classify_task("Create new API endpoint")
        self.assertEqual(task_type, TaskType.BUILD)
    
    def test_review_task_classification(self):
        """Test review task classification"""
        task_type, security, complexity = classify_task("Review code for security vulnerabilities")
        self.assertEqual(task_type, TaskType.REVIEW)
        
        task_type, security, complexity = classify_task("Audit database access patterns")
        self.assertEqual(task_type, TaskType.REVIEW)
    
    def test_security_level_classification(self):
        """Test security level classification"""
        _, security, _ = classify_task("Public demo application")
        self.assertEqual(security, SecurityLevel.LOW)
        
        _, security, _ = classify_task("Internal company tool")  
        self.assertEqual(security, SecurityLevel.HIGH)
        
        _, security, _ = classify_task("Critical production security system")
        self.assertEqual(security, SecurityLevel.CRITICAL)
    
    def test_complexity_level_classification(self):
        """Test complexity level classification"""
        _, _, complexity = classify_task("Simple bug fix")
        self.assertEqual(complexity, ComplexityLevel.SIMPLE)
        
        _, _, complexity = classify_task("Basic feature implementation")
        self.assertEqual(complexity, ComplexityLevel.SIMPLE)
        
        _, _, complexity = classify_task("Complex enterprise integration")
        self.assertEqual(complexity, ComplexityLevel.COMPLEX)
        
        _, _, complexity = classify_task("Expert-level performance optimization")
        self.assertEqual(complexity, ComplexityLevel.EXPERT)


class TestRoutingIntelligenceLayer(unittest.TestCase):
    """Test the core routing intelligence functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Use temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        self.intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
        
        # Create test task context
        self.test_task = TaskContext(
            task_id="test_task_1",
            task_type=TaskType.BUILD,
            security_level=SecurityLevel.MEDIUM,
            complexity_level=ComplexityLevel.MODERATE,
            description="Test task for unit testing",
            metadata={"component": "auth", "domain": "backend"},
            timestamp=datetime.now()
        )
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_agent_initialization(self):
        """Test that default agents are properly initialized"""
        self.assertEqual(len(self.intelligence.agents), 5)
        self.assertIn(AgentType.CHATGPT_DESIGN, self.intelligence.agents)
        self.assertIn(AgentType.CLAUDE_BUILD, self.intelligence.agents)
        self.assertIn(AgentType.GITHUB_COPILOT_REVIEW, self.intelligence.agents)
    
    def test_agent_selection_basic(self):
        """Test basic agent selection functionality"""
        agent, confidence = self.intelligence.select_agent(self.test_task)
        
        self.assertIsInstance(agent, AgentType)
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
    
    def test_design_task_routing(self):
        """Test that design tasks are routed to appropriate agents"""
        design_task = TaskContext(
            task_id="design_test",
            task_type=TaskType.DESIGN,
            security_level=SecurityLevel.MEDIUM,
            complexity_level=ComplexityLevel.MODERATE,
            description="Design system architecture",
            metadata={},
            timestamp=datetime.now()
        )
        
        agent, confidence = self.intelligence.select_agent(design_task)
        
        # Should prefer ChatGPT for design tasks
        self.assertEqual(agent, AgentType.CHATGPT_DESIGN)
        self.assertGreater(confidence, 0.5)
    
    def test_build_task_routing(self):
        """Test that build tasks are routed to appropriate agents"""
        build_task = TaskContext(
            task_id="build_test", 
            task_type=TaskType.BUILD,
            security_level=SecurityLevel.MEDIUM,
            complexity_level=ComplexityLevel.MODERATE,
            description="Implement API endpoints",
            metadata={},
            timestamp=datetime.now()
        )
        
        agent, confidence = self.intelligence.select_agent(build_task)
        
        # Should prefer Claude for build tasks
        self.assertEqual(agent, AgentType.CLAUDE_BUILD)
        self.assertGreater(confidence, 0.5)
    
    def test_security_task_routing(self):
        """Test that security tasks are routed to appropriate agents"""
        security_task = TaskContext(
            task_id="security_test",
            task_type=TaskType.SECURITY,
            security_level=SecurityLevel.CRITICAL,
            complexity_level=ComplexityLevel.EXPERT,
            description="Security audit of authentication system",
            metadata={},
            timestamp=datetime.now()
        )
        
        agent, confidence = self.intelligence.select_agent(security_task)
        
        # Should prefer specialized security or Copilot for security tasks
        self.assertIn(agent, [AgentType.SPECIALIZED_SECURITY, AgentType.GITHUB_COPILOT_REVIEW])
        self.assertGreater(confidence, 0.4)
    
    def test_agent_filtering_security_clearance(self):
        """Test that agents without sufficient security clearance are filtered out"""
        critical_task = TaskContext(
            task_id="critical_test",
            task_type=TaskType.BUILD,
            security_level=SecurityLevel.CRITICAL,
            complexity_level=ComplexityLevel.SIMPLE,
            description="Critical security implementation",
            metadata={},
            timestamp=datetime.now()
        )
        
        eligible_agents = self.intelligence._filter_eligible_agents(critical_task)
        
        # Only agents with CRITICAL clearance should be eligible
        for agent_type in eligible_agents:
            capability = self.intelligence.agents[agent_type]
            self.assertGreaterEqual(
                self.intelligence._security_level_value(capability.security_clearance),
                self.intelligence._security_level_value(SecurityLevel.CRITICAL)
            )
    
    def test_agent_filtering_complexity(self):
        """Test that agents without sufficient complexity capability are filtered out"""
        expert_task = TaskContext(
            task_id="expert_test",
            task_type=TaskType.BUILD,
            security_level=SecurityLevel.LOW,
            complexity_level=ComplexityLevel.EXPERT,
            description="Expert-level optimization task",
            metadata={},
            timestamp=datetime.now()
        )
        
        eligible_agents = self.intelligence._filter_eligible_agents(expert_task)
        
        # Only agents with EXPERT capability should be eligible
        for agent_type in eligible_agents:
            capability = self.intelligence.agents[agent_type]
            self.assertGreaterEqual(
                self.intelligence._complexity_level_value(capability.complexity_rating),
                self.intelligence._complexity_level_value(ComplexityLevel.EXPERT)
            )
    
    def test_outcome_recording(self):
        """Test recording and storage of task outcomes"""
        initial_count = len(self.intelligence.outcome_history)
        
        # Record a successful outcome
        self.intelligence.record_outcome(
            task_id="test_outcome",
            agent_type=AgentType.CLAUDE_BUILD,
            success=True,
            execution_time=300.0,
            quality_score=0.9,
            feedback="Task completed successfully"
        )
        
        self.assertEqual(len(self.intelligence.outcome_history), initial_count + 1)
        
        # Check the recorded outcome
        outcome = self.intelligence.outcome_history[-1]
        self.assertEqual(outcome.task_id, "test_outcome")
        self.assertEqual(outcome.agent_type, AgentType.CLAUDE_BUILD)
        self.assertTrue(outcome.success)
        self.assertEqual(outcome.execution_time, 300.0)
        self.assertEqual(outcome.quality_score, 0.9)
    
    def test_learning_from_outcomes(self):
        """Test that the system learns from historical outcomes"""
        # Record multiple outcomes for an agent
        for i in range(5):
            self.intelligence.record_outcome(
                task_id=f"learning_test_{i}",
                agent_type=AgentType.CLAUDE_BUILD,
                success=True,
                execution_time=200.0 + (i * 10),  # Increasing execution time
                quality_score=0.95 - (i * 0.02),  # Decreasing quality
                feedback=f"Test outcome {i}"
            )
        
        # Check that metrics are updated
        claude_metrics = self.intelligence.agents[AgentType.CLAUDE_BUILD].performance_metrics
        
        # Success rate should be high (all were successful)
        self.assertGreater(claude_metrics["success_rate"], 0.9)
        
        # Quality score should reflect the recorded outcomes
        self.assertLess(claude_metrics["quality_score"], 0.95)  # Should be lower due to declining quality
    
    def test_fallback_agent_selection(self):
        """Test fallback agent selection when no eligible agents"""
        # Create task that no agent can handle (impossible requirements)
        impossible_task = TaskContext(
            task_id="impossible_test",
            task_type=TaskType.BUILD,
            security_level=SecurityLevel.CRITICAL,
            complexity_level=ComplexityLevel.EXPERT,
            description="Impossible task for testing",
            metadata={},
            timestamp=datetime.now()
        )
        
        # Temporarily disable all agents
        for agent in self.intelligence.agents.values():
            agent.availability = False
        
        try:
            agent, confidence = self.intelligence.select_agent(impossible_task)
            
            # Should return a fallback agent with low confidence
            self.assertIsInstance(agent, AgentType)
            self.assertLessEqual(confidence, 0.5)  # Low confidence for fallback
            
        finally:
            # Restore agent availability
            for agent in self.intelligence.agents.values():
                agent.availability = True
    
    def test_task_signature_generation(self):
        """Test task signature generation for similarity comparison"""
        signature1 = self.intelligence._generate_task_signature(self.test_task)
        
        # Create similar task
        similar_task = TaskContext(
            task_id="similar_test",
            task_type=TaskType.BUILD,  # Same type
            security_level=SecurityLevel.MEDIUM,  # Same security
            complexity_level=ComplexityLevel.MODERATE,  # Same complexity
            description="Different description but same characteristics",
            metadata={"component": "auth", "domain": "backend"},  # Same metadata
            timestamp=datetime.now()
        )
        
        signature2 = self.intelligence._generate_task_signature(similar_task)
        
        # Signatures should be the same for similar tasks
        self.assertEqual(signature1, signature2)
        
        # Create different task
        different_task = TaskContext(
            task_id="different_test",
            task_type=TaskType.REVIEW,  # Different type
            security_level=SecurityLevel.HIGH,  # Different security
            complexity_level=ComplexityLevel.COMPLEX,  # Different complexity
            description="Completely different task",
            metadata={"component": "ui", "domain": "frontend"},  # Different metadata
            timestamp=datetime.now()
        )
        
        signature3 = self.intelligence._generate_task_signature(different_task)
        
        # Signature should be different
        self.assertNotEqual(signature1, signature3)
    
    def test_performance_trend_analysis(self):
        """Test recent performance trend analysis"""
        # Record outcomes with improving trend
        base_time = datetime.now() - timedelta(days=20)
        
        for i in range(10):
            success = i >= 3  # First 3 fail, rest succeed (improving trend)
            self.intelligence.outcome_history.append(
                OutcomeRecord(
                    task_id=f"trend_test_{i}",
                    agent_type=AgentType.CLAUDE_BUILD,
                    success=success,
                    execution_time=300.0,
                    quality_score=0.8 if success else 0.4,
                    feedback="Trend test",
                    timestamp=base_time + timedelta(days=i*2)
                )
            )
        
        trend_score = self.intelligence._get_recent_performance_trend(AgentType.CLAUDE_BUILD)
        
        # Should detect improving trend
        self.assertGreater(trend_score, 0.5)  # Above neutral indicates improvement
    
    def test_memory_persistence(self):
        """Test that outcomes and tasks are persisted to disk"""
        # Record some data
        self.intelligence.record_outcome(
            task_id="persistence_test",
            agent_type=AgentType.CLAUDE_BUILD,
            success=True,
            execution_time=250.0,
            quality_score=0.85,
            feedback="Persistence test"
        )
        
        # Create new instance with same memory file
        new_intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
        
        # Check that data was loaded
        self.assertGreater(len(new_intelligence.outcome_history), 0)
        
        # Find our test outcome
        test_outcome = None
        for outcome in new_intelligence.outcome_history:
            if outcome.task_id == "persistence_test":
                test_outcome = outcome
                break
        
        self.assertIsNotNone(test_outcome)
        self.assertEqual(test_outcome.agent_type, AgentType.CLAUDE_BUILD)
        self.assertTrue(test_outcome.success)
        self.assertEqual(test_outcome.execution_time, 250.0)
    
    def test_system_status_reporting(self):
        """Test system status and metrics reporting"""
        # Add some test data
        self.intelligence.record_outcome(
            task_id="status_test",
            agent_type=AgentType.CLAUDE_BUILD,
            success=True,
            execution_time=200.0,
            quality_score=0.9,
            feedback="Status test"
        )
        
        status = self.intelligence.get_agent_status()
        
        # Check status structure
        self.assertIn('agents', status)
        self.assertIn('system_metrics', status)
        
        # Check system metrics
        self.assertIn('total_tasks', status['system_metrics'])
        self.assertIn('total_outcomes', status['system_metrics'])
        self.assertIn('overall_success_rate', status['system_metrics'])
        
        # Check agent status
        for agent_name in status['agents']:
            agent_info = status['agents'][agent_name]
            self.assertIn('availability', agent_info)
            self.assertIn('performance_metrics', agent_info)
            self.assertIn('recent_tasks', agent_info)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_empty_task_description(self):
        """Test handling of empty task descriptions"""
        task_type, security, complexity = classify_task("")
        
        # Should return defaults
        self.assertIsInstance(task_type, TaskType)
        self.assertIsInstance(security, SecurityLevel)
        self.assertIsInstance(complexity, ComplexityLevel)
    
    def test_invalid_quality_score(self):
        """Test handling of invalid quality scores"""
        # Quality score out of range should be accepted but clamped internally
        self.intelligence.record_outcome(
            task_id="invalid_quality_test",
            agent_type=AgentType.CLAUDE_BUILD,
            success=True,
            execution_time=300.0,
            quality_score=1.5,  # Invalid (>1.0)
            feedback="Invalid quality test"
        )
        
        # Should not crash and should record the outcome
        self.assertGreater(len(self.intelligence.outcome_history), 0)
    
    def test_corrupted_memory_file(self):
        """Test handling of corrupted memory file"""
        # Write invalid JSON to memory file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Should not crash when loading
        intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
        
        # Should initialize with defaults
        self.assertEqual(len(intelligence.outcome_history), 0)
        self.assertGreater(len(intelligence.agents), 0)
    
    def test_no_historical_data(self):
        """Test agent selection with no historical data"""
        # Fresh intelligence layer should still work
        fresh_intelligence = RoutingIntelligenceLayer(memory_file="/tmp/nonexistent_file.json")
        
        task = TaskContext(
            task_id="no_history_test",
            task_type=TaskType.BUILD,
            security_level=SecurityLevel.MEDIUM,
            complexity_level=ComplexityLevel.MODERATE,
            description="Test with no history",
            metadata={},
            timestamp=datetime.now()
        )
        
        agent, confidence = fresh_intelligence.select_agent(task)
        
        # Should still select an agent
        self.assertIsInstance(agent, AgentType)
        self.assertGreaterEqual(confidence, 0.0)


if __name__ == '__main__':
    unittest.main()