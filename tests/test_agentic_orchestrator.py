#!/usr/bin/env python3
"""
API tests for the Agentic Orchestrator

Tests cover:
- Task request processing and agent assignment
- Integration with routing intelligence layer
- Task completion recording and feedback
- Orchestrator API behavior and error handling
- Compatibility with existing STANDARDS.md workflows
"""

import unittest
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from src.agentic_orchestrator import (
    AgenticOrchestrator, TaskRequest, AgentAssignment,
    assign_design_task, assign_build_task, assign_review_task,
    record_task_completion, get_orchestrator
)
from src.agent_intelligence import (
    TaskType, SecurityLevel, ComplexityLevel, AgentType
)


class TestTaskRequest(unittest.TestCase):
    """Test TaskRequest data structure and validation"""
    
    def test_task_request_creation(self):
        """Test basic task request creation"""
        request = TaskRequest(
            description="Test task description",
            context={"key": "value"},
            requester="test_user"
        )
        
        self.assertEqual(request.description, "Test task description")
        self.assertEqual(request.context, {"key": "value"})
        self.assertEqual(request.requester, "test_user")
        self.assertEqual(request.priority, "medium")  # Default
        self.assertIsNone(request.deadline)  # Default
    
    def test_task_request_with_deadline(self):
        """Test task request with deadline"""
        deadline = datetime.now() + timedelta(hours=24)
        request = TaskRequest(
            description="Urgent task",
            context={},
            requester="manager",
            priority="high",
            deadline=deadline
        )
        
        self.assertEqual(request.priority, "high")
        self.assertEqual(request.deadline, deadline)


class TestAgenticOrchestrator(unittest.TestCase):
    """Test the main orchestrator functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary memory file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Patch the routing intelligence to use our temp file
        with patch('src.agentic_orchestrator.get_routing_intelligence') as mock_get_routing:
            from src.agent_intelligence import RoutingIntelligenceLayer
            mock_intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
            mock_get_routing.return_value = mock_intelligence
            
            self.orchestrator = AgenticOrchestrator()
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_process_task_request_basic(self):
        """Test basic task request processing"""
        request = TaskRequest(
            description="Implement user authentication",
            context={"component": "auth", "domain": "backend"},
            requester="developer"
        )
        
        assignment = self.orchestrator.process_task_request(request)
        
        # Check assignment structure
        self.assertIsInstance(assignment, AgentAssignment)
        self.assertIsInstance(assignment.task_id, str)
        self.assertIsInstance(assignment.assigned_agent, AgentType)
        self.assertIsInstance(assignment.confidence_score, float)
        self.assertIsInstance(assignment.fallback_agents, list)
        self.assertIsInstance(assignment.reasoning, str)
        self.assertIsInstance(assignment.estimated_duration, float)
        
        # Check confidence score is valid
        self.assertGreaterEqual(assignment.confidence_score, 0.0)
        self.assertLessEqual(assignment.confidence_score, 1.0)
        
        # Check that task is tracked
        self.assertIn(assignment.task_id, self.orchestrator.active_tasks)
        self.assertIn(assignment.task_id, self.orchestrator.agent_assignments)
    
    def test_design_task_assignment(self):
        """Test that design tasks are properly assigned"""
        request = TaskRequest(
            description="Design REST API for user management system",
            context={"task_hint": "design"},
            requester="architect"
        )
        
        assignment = self.orchestrator.process_task_request(request)
        
        # Should assign to ChatGPT for design tasks
        self.assertEqual(assignment.assigned_agent, AgentType.CHATGPT_DESIGN)
        
        # Should have high confidence for clear design task
        self.assertGreater(assignment.confidence_score, 0.6)
        
        # Reasoning should mention design
        self.assertIn("design", assignment.reasoning.lower())
    
    def test_build_task_assignment(self):
        """Test that build tasks are properly assigned"""
        request = TaskRequest(
            description="Implement JWT authentication middleware",
            context={"task_hint": "build"},
            requester="developer"
        )
        
        assignment = self.orchestrator.process_task_request(request)
        
        # Should assign to Claude for build tasks
        self.assertEqual(assignment.assigned_agent, AgentType.CLAUDE_BUILD)
        
        # Should have high confidence for clear build task
        self.assertGreater(assignment.confidence_score, 0.6)
        
        # Reasoning should mention implementation/development
        reasoning_lower = assignment.reasoning.lower()
        self.assertTrue(
            any(keyword in reasoning_lower for keyword in ["implementation", "development", "build"])
        )
    
    def test_review_task_assignment(self):
        """Test that review tasks are properly assigned"""
        request = TaskRequest(
            description="Review security vulnerabilities in authentication code",
            context={"task_hint": "review"},
            requester="security_team"
        )
        
        assignment = self.orchestrator.process_task_request(request)
        
        # Should assign to review agent (Copilot or specialized security)
        self.assertIn(assignment.assigned_agent, [
            AgentType.GITHUB_COPILOT_REVIEW,
            AgentType.SPECIALIZED_SECURITY
        ])
        
        # Should have reasonable confidence
        self.assertGreater(assignment.confidence_score, 0.4)
        
        # Reasoning should mention review or security
        reasoning_lower = assignment.reasoning.lower()
        self.assertTrue(
            any(keyword in reasoning_lower for keyword in ["review", "security"])
        )
    
    def test_security_level_impact(self):
        """Test that security level affects agent assignment"""
        # High security task
        high_security_request = TaskRequest(
            description="Implement critical security authentication for production",
            context={"environment": "production", "security": "critical"},
            requester="security_architect"
        )
        
        assignment = self.orchestrator.process_task_request(high_security_request)
        
        # Should assign to agent with high security clearance
        agent_capability = self.orchestrator.intelligence_layer.agents[assignment.assigned_agent]
        self.assertIn(agent_capability.security_clearance, [
            SecurityLevel.HIGH, SecurityLevel.CRITICAL
        ])
    
    def test_complexity_level_impact(self):
        """Test that complexity level affects agent assignment"""
        # Expert level task
        expert_request = TaskRequest(
            description="Expert-level performance optimization of critical system components",
            context={"performance": "critical", "optimization": "expert"},
            requester="senior_architect"
        )
        
        assignment = self.orchestrator.process_task_request(expert_request)
        
        # Should assign to agent capable of expert-level work
        agent_capability = self.orchestrator.intelligence_layer.agents[assignment.assigned_agent]
        self.assertIn(agent_capability.complexity_rating, [
            ComplexityLevel.COMPLEX, ComplexityLevel.EXPERT
        ])
    
    def test_fallback_agent_generation(self):
        """Test that appropriate fallback agents are generated"""
        request = TaskRequest(
            description="Build API endpoints for data access",
            context={},
            requester="developer"
        )
        
        assignment = self.orchestrator.process_task_request(request)
        
        # Should have fallback agents
        self.assertIsInstance(assignment.fallback_agents, list)
        
        # Fallbacks should be different from primary agent
        self.assertNotIn(assignment.assigned_agent.value, assignment.fallback_agents)
        
        # Should not have too many fallbacks
        self.assertLessEqual(len(assignment.fallback_agents), 3)
    
    def test_duration_estimation(self):
        """Test task duration estimation"""
        # Simple task
        simple_request = TaskRequest(
            description="Simple bug fix in authentication",
            context={},
            requester="developer"
        )
        
        simple_assignment = self.orchestrator.process_task_request(simple_request)
        
        # Complex task
        complex_request = TaskRequest(
            description="Complex enterprise-scale integration with multiple external systems",
            context={},
            requester="architect"
        )
        
        complex_assignment = self.orchestrator.process_task_request(complex_request)
        
        # Complex task should have longer estimated duration
        self.assertGreater(
            complex_assignment.estimated_duration,
            simple_assignment.estimated_duration
        )
        
        # Both should be reasonable durations (not negative, not too large)
        self.assertGreater(simple_assignment.estimated_duration, 0)
        self.assertLess(simple_assignment.estimated_duration, 7200)  # Less than 2 hours
        self.assertLess(complex_assignment.estimated_duration, 14400)  # Less than 4 hours
    
    def test_task_completion_recording(self):
        """Test task completion recording and cleanup"""
        request = TaskRequest(
            description="Test task for completion",
            context={},
            requester="tester"
        )
        
        assignment = self.orchestrator.process_task_request(request)
        task_id = assignment.task_id
        
        # Verify task is active
        self.assertIn(task_id, self.orchestrator.active_tasks)
        self.assertIn(task_id, self.orchestrator.agent_assignments)
        
        # Complete the task
        self.orchestrator.complete_task(
            task_id=task_id,
            success=True,
            execution_time=300.0,
            quality_score=0.85,
            feedback="Task completed successfully"
        )
        
        # Verify task is cleaned up
        self.assertNotIn(task_id, self.orchestrator.active_tasks)
        self.assertNotIn(task_id, self.orchestrator.agent_assignments)
        
        # Verify outcome was recorded in intelligence layer
        outcomes = self.orchestrator.intelligence_layer.outcome_history
        task_outcomes = [o for o in outcomes if o.task_id == task_id]
        self.assertEqual(len(task_outcomes), 1)
        
        outcome = task_outcomes[0]
        self.assertEqual(outcome.agent_type, assignment.assigned_agent)
        self.assertTrue(outcome.success)
        self.assertEqual(outcome.execution_time, 300.0)
        self.assertEqual(outcome.quality_score, 0.85)
    
    def test_task_status_retrieval(self):
        """Test task status retrieval"""
        request = TaskRequest(
            description="Task for status testing",
            context={"test": "status"},
            requester="tester"
        )
        
        assignment = self.orchestrator.process_task_request(request)
        task_id = assignment.task_id
        
        status = self.orchestrator.get_task_status(task_id)
        
        # Check status structure
        self.assertIn("task_id", status)
        self.assertIn("description", status)
        self.assertIn("task_type", status)
        self.assertIn("security_level", status)
        self.assertIn("complexity_level", status)
        self.assertIn("assigned_agent", status)
        self.assertIn("confidence_score", status)
        self.assertIn("estimated_duration", status)
        self.assertIn("start_time", status)
        self.assertIn("status", status)
        
        # Check values
        self.assertEqual(status["task_id"], task_id)
        self.assertEqual(status["description"], "Task for status testing")
        self.assertEqual(status["assigned_agent"], assignment.assigned_agent.value)
        self.assertEqual(status["status"], "in_progress")
    
    def test_nonexistent_task_status(self):
        """Test status retrieval for nonexistent task"""
        status = self.orchestrator.get_task_status("nonexistent_task_id")
        
        self.assertIn("error", status)
        self.assertEqual(status["error"], "Task not found")
    
    def test_system_status_reporting(self):
        """Test system status reporting"""
        # Create some tasks first
        for i in range(3):
            request = TaskRequest(
                description=f"Test task {i}",
                context={},
                requester="tester"
            )
            self.orchestrator.process_task_request(request)
        
        status = self.orchestrator.get_system_status()
        
        # Check system status structure
        self.assertIn("active_tasks", status)
        self.assertIn("orchestrator_version", status)
        self.assertIn("intelligence_enabled", status)
        self.assertIn("learning_enabled", status)
        self.assertIn("agents", status)
        self.assertIn("system_metrics", status)
        
        # Check values
        self.assertEqual(status["active_tasks"], 3)
        self.assertEqual(status["orchestrator_version"], "1.0")
        self.assertTrue(status["intelligence_enabled"])
        self.assertTrue(status["learning_enabled"])


class TestIntegrationFunctions(unittest.TestCase):
    """Test the integration functions for backward compatibility"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Reset singleton instance for testing
        import src.agentic_orchestrator
        src.agentic_orchestrator._orchestrator = None
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    @patch('src.agentic_orchestrator.get_routing_intelligence')
    def test_assign_design_task(self, mock_get_routing):
        """Test design task assignment integration function"""
        from src.agent_intelligence import RoutingIntelligenceLayer
        mock_intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
        mock_get_routing.return_value = mock_intelligence
        
        assignment = assign_design_task(
            description="Design user interface for mobile app",
            context={"platform": "mobile"},
            requester="ui_designer"
        )
        
        self.assertIsInstance(assignment, AgentAssignment)
        self.assertEqual(assignment.assigned_agent, AgentType.CHATGPT_DESIGN)
        self.assertIn("design", assignment.reasoning.lower())
    
    @patch('src.agentic_orchestrator.get_routing_intelligence')
    def test_assign_build_task(self, mock_get_routing):
        """Test build task assignment integration function"""
        from src.agent_intelligence import RoutingIntelligenceLayer
        mock_intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
        mock_get_routing.return_value = mock_intelligence
        
        assignment = assign_build_task(
            description="Implement database migration scripts",
            context={"database": "postgresql"},
            requester="backend_developer"
        )
        
        self.assertIsInstance(assignment, AgentAssignment)
        self.assertEqual(assignment.assigned_agent, AgentType.CLAUDE_BUILD)
        self.assertIn("build", assignment.reasoning.lower())
    
    @patch('src.agentic_orchestrator.get_routing_intelligence') 
    def test_assign_review_task(self, mock_get_routing):
        """Test review task assignment integration function"""
        from src.agent_intelligence import RoutingIntelligenceLayer
        mock_intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
        mock_get_routing.return_value = mock_intelligence
        
        assignment = assign_review_task(
            description="Review code for potential security vulnerabilities",
            context={"security_focus": True},
            requester="security_reviewer"
        )
        
        self.assertIsInstance(assignment, AgentAssignment)
        self.assertIn(assignment.assigned_agent, [
            AgentType.GITHUB_COPILOT_REVIEW,
            AgentType.SPECIALIZED_SECURITY
        ])
        reasoning_lower = assignment.reasoning.lower()
        self.assertTrue(
            any(keyword in reasoning_lower for keyword in ["review", "security"])
        )
    
    @patch('src.agentic_orchestrator.get_routing_intelligence')
    def test_record_task_completion_integration(self, mock_get_routing):
        """Test task completion recording integration function"""
        from src.agent_intelligence import RoutingIntelligenceLayer
        mock_intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
        mock_get_routing.return_value = mock_intelligence
        
        # First create a task
        assignment = assign_build_task("Test task for completion")
        
        # Record completion
        record_task_completion(
            task_id=assignment.task_id,
            success=True,
            execution_time=250.0,
            quality_score=0.9,
            feedback="Integration test completion"
        )
        
        # Verify outcome was recorded
        outcomes = mock_intelligence.outcome_history
        task_outcomes = [o for o in outcomes if o.task_id == assignment.task_id]
        self.assertEqual(len(task_outcomes), 1)
        
        outcome = task_outcomes[0]
        self.assertTrue(outcome.success)
        self.assertEqual(outcome.execution_time, 250.0)
        self.assertEqual(outcome.quality_score, 0.9)
    
    def test_orchestrator_singleton(self):
        """Test that get_orchestrator returns singleton instance"""
        orchestrator1 = get_orchestrator()
        orchestrator2 = get_orchestrator()
        
        # Should be the same instance
        self.assertIs(orchestrator1, orchestrator2)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        with patch('src.agentic_orchestrator.get_routing_intelligence') as mock_get_routing:
            from src.agent_intelligence import RoutingIntelligenceLayer
            mock_intelligence = RoutingIntelligenceLayer(memory_file=self.temp_file.name)
            mock_get_routing.return_value = mock_intelligence
            
            self.orchestrator = AgenticOrchestrator()
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_empty_task_description(self):
        """Test handling of empty task description"""
        request = TaskRequest(
            description="",
            context={},
            requester="tester"
        )
        
        # Should not crash and should assign an agent
        assignment = self.orchestrator.process_task_request(request)
        self.assertIsInstance(assignment, AgentAssignment)
    
    def test_none_context(self):
        """Test handling of None context"""
        request = TaskRequest(
            description="Test task with no context",
            context=None,
            requester="tester"
        )
        
        # Should handle gracefully (context becomes {})
        assignment = self.orchestrator.process_task_request(request)
        self.assertIsInstance(assignment, AgentAssignment)
    
    def test_invalid_task_completion(self):
        """Test completion recording for nonexistent task"""
        # Should handle gracefully without crashing
        self.orchestrator.complete_task(
            task_id="nonexistent_task",
            success=True,
            execution_time=100.0,
            quality_score=0.8
        )
        
        # Should not add to outcome history since task doesn't exist
        outcomes = self.orchestrator.intelligence_layer.outcome_history
        nonexistent_outcomes = [o for o in outcomes if o.task_id == "nonexistent_task"]
        self.assertEqual(len(nonexistent_outcomes), 0)


if __name__ == '__main__':
    unittest.main()