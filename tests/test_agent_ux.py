#!/usr/bin/env python3
"""
UX tests for the Dynamic Agent Selection System

Tests cover:
- End-to-end user workflows
- CLI tool functionality and user experience
- Integration with existing STANDARDS.md workflows
- System behavior under real-world scenarios
- User-facing error messages and feedback
"""

import unittest
import tempfile
import os
import sys
import io
import subprocess
from unittest.mock import patch, MagicMock
from contextlib import contextmanager

from src.agent_cli import (
    simulate_task, run_batch_simulation, show_system_status,
    interactive_mode, main
)
from src.agentic_orchestrator import get_orchestrator
from src.agent_intelligence import AgentType


@contextmanager
def capture_stdout():
    """Context manager to capture stdout for testing CLI output"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    try:
        yield captured_output
    finally:
        sys.stdout = old_stdout


class TestCLITaskSimulation(unittest.TestCase):
    """Test CLI task simulation functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Reset singleton for clean testing
        import src.agentic_orchestrator
        src.agentic_orchestrator._orchestrator = None
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_simulate_design_task_ux(self):
        """Test UX of simulating a design task"""
        with capture_stdout() as output:
            result = simulate_task(
                description="Design REST API for user management",
                task_type="design",
                success_rate=1.0,
                duration=200.0
            )
        
        output_text = output.getvalue()
        
        # Check that user gets clear feedback
        self.assertIn("Task assigned", output_text)
        self.assertIn("Confidence:", output_text)
        self.assertIn("Reasoning:", output_text)
        self.assertIn("Estimated duration:", output_text)
        
        # Check result structure
        self.assertIn("task_id", result)
        self.assertIn("assigned_agent", result)
        self.assertIn("confidence", result)
        self.assertIn("success", result)
        self.assertIn("execution_time", result)
        self.assertIn("quality_score", result)
        
        # Should assign to ChatGPT for design
        self.assertEqual(result["assigned_agent"], AgentType.CHATGPT_DESIGN.value)
    
    def test_simulate_build_task_ux(self):
        """Test UX of simulating a build task"""
        with capture_stdout() as output:
            result = simulate_task(
                description="Implement JWT authentication middleware",
                task_type="build",
                success_rate=1.0,
                duration=400.0
            )
        
        output_text = output.getvalue()
        
        # Check user feedback quality
        self.assertIn("Task assigned", output_text)
        self.assertIn(AgentType.CLAUDE_BUILD.value, output_text)
        
        # Should assign to Claude for build
        self.assertEqual(result["assigned_agent"], AgentType.CLAUDE_BUILD.value)
        
        # Check confidence is reasonable
        self.assertGreater(result["confidence"], 0.5)
    
    def test_simulate_review_task_ux(self):
        """Test UX of simulating a review task"""
        with capture_stdout() as output:
            result = simulate_task(
                description="Review security vulnerabilities in authentication code",
                task_type="review",
                success_rate=0.9,
                duration=150.0
            )
        
        output_text = output.getvalue()
        
        # Check output includes reasoning
        self.assertIn("Reasoning:", output_text)
        reasoning_in_output = True
        for line in output_text.split('\n'):
            if line.startswith("Reasoning:"):
                # Should mention review or security
                line_lower = line.lower()
                self.assertTrue(
                    any(keyword in line_lower for keyword in ["review", "security"])
                )
                break
        else:
            self.fail("Reasoning not found in output")
        
        # Should assign to review-capable agent
        self.assertIn(result["assigned_agent"], [
            AgentType.GITHUB_COPILOT_REVIEW.value,
            AgentType.SPECIALIZED_SECURITY.value
        ])
    
    def test_auto_task_classification_ux(self):
        """Test UX of automatic task classification"""
        with capture_stdout() as output:
            result = simulate_task(
                description="Create database schema for user management system",
                task_type="auto",  # Let system decide
                success_rate=1.0,
                duration=300.0
            )
        
        output_text = output.getvalue()
        
        # Should provide clear assignment information
        self.assertIn("Task assigned:", output_text)
        self.assertIn("Confidence:", output_text)
        
        # System should classify this as design task
        self.assertEqual(result["assigned_agent"], AgentType.CHATGPT_DESIGN.value)
    
    def test_low_confidence_task_ux(self):
        """Test UX when system has low confidence in assignment"""
        # Create a very ambiguous task description
        with capture_stdout() as output:
            result = simulate_task(
                description="Do something",  # Very vague
                task_type="auto",
                success_rate=0.5,
                duration=100.0
            )
        
        output_text = output.getvalue()
        
        # Should still provide assignment but may have lower confidence
        self.assertIn("Task assigned:", output_text)
        self.assertIn("Confidence:", output_text)
        
        # Check that result is still valid
        self.assertIsInstance(result["confidence"], float)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)


class TestBatchSimulation(unittest.TestCase):
    """Test batch simulation functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Reset singleton
        import src.agentic_orchestrator
        src.agentic_orchestrator._orchestrator = None
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_batch_simulation_ux(self):
        """Test UX of batch simulation"""
        with capture_stdout() as output:
            run_batch_simulation(count=5, task_types=["design", "build"])
        
        output_text = output.getvalue()
        
        # Should show progress for each task
        self.assertIn("Task 1:", output_text)
        self.assertIn("Task 5:", output_text)
        
        # Should show summary statistics
        self.assertIn("SIMULATION SUMMARY", output_text)
        self.assertIn("Success Rate:", output_text)
        self.assertIn("Average Confidence:", output_text)
        self.assertIn("Average Quality:", output_text)
        self.assertIn("Agent Usage:", output_text)
        
        # Should show agent distribution
        self.assertTrue(
            any(agent.value in output_text for agent in AgentType)
        )
    
    def test_single_task_type_batch(self):
        """Test batch simulation with single task type"""
        with capture_stdout() as output:
            run_batch_simulation(count=3, task_types=["design"])
        
        output_text = output.getvalue()
        
        # Should complete without errors
        self.assertIn("SIMULATION SUMMARY", output_text)
        
        # Should show design agent usage predominantly
        self.assertIn(AgentType.CHATGPT_DESIGN.value, output_text)
    
    def test_empty_batch_simulation(self):
        """Test batch simulation with zero tasks"""
        with capture_stdout() as output:
            run_batch_simulation(count=0, task_types=["build"])
        
        output_text = output.getvalue()
        
        # Should handle gracefully
        self.assertIn("Running batch simulation with 0 tasks", output_text)


class TestSystemStatusDisplay(unittest.TestCase):
    """Test system status display functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Reset singleton and create some test data
        import src.agentic_orchestrator
        src.agentic_orchestrator._orchestrator = None
        
        # Create some test activity
        orchestrator = get_orchestrator()
        from src.agentic_orchestrator import TaskRequest
        
        request = TaskRequest(
            description="Test task for status display",
            context={},
            requester="test_user"
        )
        assignment = orchestrator.process_task_request(request)
        orchestrator.complete_task(
            task_id=assignment.task_id,
            success=True,
            execution_time=200.0,
            quality_score=0.85,
            feedback="Status test completed"
        )
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_system_status_display_ux(self):
        """Test UX of system status display"""
        with capture_stdout() as output:
            show_system_status()
        
        output_text = output.getvalue()
        
        # Should show clear headers and sections
        self.assertIn("AGENTIC ENGINEERING SYSTEM STATUS", output_text)
        self.assertIn("SYSTEM METRICS", output_text)
        self.assertIn("AGENT STATUS", output_text)
        
        # Should show version information
        self.assertIn("Orchestrator Version:", output_text)
        self.assertIn("Intelligence Enabled:", output_text)
        self.assertIn("Learning Enabled:", output_text)
        
        # Should show metrics
        self.assertIn("Total Tasks Processed:", output_text)
        self.assertIn("Overall Success Rate:", output_text)
        self.assertIn("Average Execution Time:", output_text)
        
        # Should show agent information
        for agent_type in AgentType:
            self.assertIn(agent_type.value.upper(), output_text)
    
    def test_agent_metrics_display(self):
        """Test that agent metrics are properly displayed"""
        with capture_stdout() as output:
            show_system_status()
        
        output_text = output.getvalue()
        
        # Each agent should show key metrics
        agent_sections = []
        lines = output_text.split('\n')
        current_agent = None
        
        for line in lines:
            if any(agent.value.upper() in line for agent in AgentType):
                current_agent = line.strip()
                agent_sections.append(current_agent)
        
        # Should have agent sections
        self.assertGreater(len(agent_sections), 0)
        
        # Should show availability and performance metrics
        self.assertIn("Available:", output_text)
        self.assertIn("Success Rate:", output_text)
        self.assertIn("Avg Quality:", output_text)
        self.assertIn("Recent Tasks:", output_text)


class TestInteractiveMode(unittest.TestCase):
    """Test interactive mode functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Reset singleton
        import src.agentic_orchestrator
        src.agentic_orchestrator._orchestrator = None
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    @patch('builtins.input')
    def test_interactive_mode_task_processing(self, mock_input):
        """Test interactive mode task processing"""
        # Simulate user input sequence
        mock_input.side_effect = [
            "Design user authentication system",  # Task description
            "quit"  # Exit command
        ]
        
        with capture_stdout() as output:
            interactive_mode()
        
        output_text = output.getvalue()
        
        # Should show welcome message
        self.assertIn("INTERACTIVE AGENT SELECTION MODE", output_text)
        
        # Should process the task
        self.assertIn("Analyzing:", output_text)
        self.assertIn("Task assigned:", output_text)
        
        # Should show goodbye message
        self.assertIn("Goodbye!", output_text)
    
    @patch('builtins.input')
    def test_interactive_mode_status_command(self, mock_input):
        """Test status command in interactive mode"""
        mock_input.side_effect = ["status", "quit"]
        
        with capture_stdout() as output:
            interactive_mode()
        
        output_text = output.getvalue()
        
        # Should show system status
        self.assertIn("AGENTIC ENGINEERING SYSTEM STATUS", output_text)
        self.assertIn("AGENT STATUS", output_text)
    
    @patch('builtins.input')
    def test_interactive_mode_empty_input(self, mock_input):
        """Test handling of empty input in interactive mode"""
        mock_input.side_effect = ["", "  ", "quit"]
        
        with capture_stdout() as output:
            interactive_mode()
        
        output_text = output.getvalue()
        
        # Should handle empty input gracefully
        self.assertIn("Goodbye!", output_text)
    
    @patch('builtins.input')
    def test_interactive_mode_keyboard_interrupt(self, mock_input):
        """Test keyboard interrupt handling in interactive mode"""
        mock_input.side_effect = KeyboardInterrupt()
        
        with capture_stdout() as output:
            interactive_mode()
        
        output_text = output.getvalue()
        
        # Should handle interrupt gracefully
        self.assertIn("Goodbye!", output_text)


class TestCLIMainFunction(unittest.TestCase):
    """Test main CLI function and argument parsing"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Reset singleton
        import src.agentic_orchestrator
        src.agentic_orchestrator._orchestrator = None
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    @patch('sys.argv', ['agent_cli.py', 'status'])
    def test_cli_status_command(self):
        """Test CLI status command"""
        with capture_stdout() as output:
            try:
                main()
            except SystemExit:
                pass  # Expected for successful CLI execution
        
        output_text = output.getvalue()
        
        # Should show status information
        self.assertIn("SYSTEM STATUS", output_text)
    
    @patch('sys.argv', ['agent_cli.py', 'simulate', 'Build user authentication'])
    def test_cli_simulate_command(self):
        """Test CLI simulate command"""
        with capture_stdout() as output:
            try:
                main()
            except SystemExit:
                pass
        
        output_text = output.getvalue()
        
        # Should show simulation results
        self.assertIn("Task assigned:", output_text)
    
    @patch('sys.argv', ['agent_cli.py', 'batch', '3'])
    def test_cli_batch_command(self):
        """Test CLI batch command"""
        with capture_stdout() as output:
            try:
                main()
            except SystemExit:
                pass
        
        output_text = output.getvalue()
        
        # Should run batch simulation
        self.assertIn("Running batch simulation", output_text)
        self.assertIn("SIMULATION SUMMARY", output_text)
    
    @patch('sys.argv', ['agent_cli.py'])
    def test_cli_no_command(self):
        """Test CLI with no command shows help"""
        with capture_stdout() as output:
            try:
                main()
            except SystemExit:
                pass
        
        output_text = output.getvalue()
        
        # Should show help information
        self.assertIn("usage:", output_text.lower())


class TestRealWorldWorkflows(unittest.TestCase):
    """Test real-world workflow scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Reset singleton
        import src.agentic_orchestrator
        src.agentic_orchestrator._orchestrator = None
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_complete_feature_development_workflow(self):
        """Test complete workflow from design to deployment"""
        orchestrator = get_orchestrator()
        from src.agentic_orchestrator import TaskRequest
        
        # Step 1: Design phase
        design_request = TaskRequest(
            description="Design REST API for user authentication system",
            context={"phase": "design", "component": "auth"},
            requester="product_manager"
        )
        
        design_assignment = orchestrator.process_task_request(design_request)
        self.assertEqual(design_assignment.assigned_agent, AgentType.CHATGPT_DESIGN)
        
        # Complete design phase
        orchestrator.complete_task(
            task_id=design_assignment.task_id,
            success=True,
            execution_time=300.0,
            quality_score=0.9,
            feedback="Design phase completed successfully"
        )
        
        # Step 2: Build phase
        build_request = TaskRequest(
            description="Implement JWT authentication endpoints based on design",
            context={"phase": "build", "component": "auth", "based_on": design_assignment.task_id},
            requester="developer"
        )
        
        build_assignment = orchestrator.process_task_request(build_request)
        self.assertEqual(build_assignment.assigned_agent, AgentType.CLAUDE_BUILD)
        
        # Complete build phase
        orchestrator.complete_task(
            task_id=build_assignment.task_id,
            success=True,
            execution_time=600.0,
            quality_score=0.85,
            feedback="Implementation completed with tests"
        )
        
        # Step 3: Review phase
        review_request = TaskRequest(
            description="Security review of authentication implementation",
            context={"phase": "review", "component": "auth", "review_type": "security"},
            requester="security_team"
        )
        
        review_assignment = orchestrator.process_task_request(review_request)
        self.assertIn(review_assignment.assigned_agent, [
            AgentType.GITHUB_COPILOT_REVIEW,
            AgentType.SPECIALIZED_SECURITY
        ])
        
        # Complete review phase
        orchestrator.complete_task(
            task_id=review_assignment.task_id,
            success=True,
            execution_time=200.0,
            quality_score=0.92,
            feedback="Security review passed with minor recommendations"
        )
        
        # Verify learning: System should have data about all three phases
        status = orchestrator.get_system_status()
        self.assertGreaterEqual(status['system_metrics']['total_outcomes'], 3)
        self.assertGreater(status['system_metrics']['overall_success_rate'], 0.9)
    
    def test_high_security_project_workflow(self):
        """Test workflow for high-security project"""
        orchestrator = get_orchestrator()
        from src.agentic_orchestrator import TaskRequest
        
        # High security task
        security_request = TaskRequest(
            description="Implement encryption for critical financial data processing",
            context={
                "security_level": "critical", 
                "domain": "financial",
                "compliance": "PCI-DSS"
            },
            requester="security_architect"
        )
        
        assignment = orchestrator.process_task_request(security_request)
        
        # Should assign to agent with high security clearance
        agent_capability = orchestrator.intelligence_layer.agents[assignment.assigned_agent]
        self.assertIn(agent_capability.security_clearance, [
            SecurityLevel.HIGH, SecurityLevel.CRITICAL
        ])
        
        # Should have high confidence for clear security task
        self.assertGreater(assignment.confidence_score, 0.6)
    
    def test_learning_adaptation_workflow(self):
        """Test that system adapts based on historical performance"""
        orchestrator = get_orchestrator()
        from src.agentic_orchestrator import TaskRequest
        
        # Create similar tasks and record varying performance
        task_template = "Implement database access layer for user management"
        
        # First few tasks - simulate poor performance for one agent
        for i in range(3):
            request = TaskRequest(
                description=f"{task_template} - iteration {i}",
                context={"iteration": i},
                requester="developer"
            )
            
            assignment = orchestrator.process_task_request(request)
            
            # Simulate declining performance
            success = i > 0  # First one fails, others succeed
            quality = 0.5 + (i * 0.2)  # Improving quality
            
            orchestrator.complete_task(
                task_id=assignment.task_id,
                success=success,
                execution_time=300.0 + (i * 50),  # Increasing time
                quality_score=min(quality, 1.0),
                feedback=f"Iteration {i} feedback"
            )
        
        # Later task should potentially be assigned differently based on learning
        final_request = TaskRequest(
            description=f"{task_template} - final iteration",
            context={"iteration": "final"},
            requester="developer"
        )
        
        final_assignment = orchestrator.process_task_request(final_request)
        
        # System should have learned and potentially adjusted assignment
        self.assertIsInstance(final_assignment, AgentAssignment)
        self.assertGreater(final_assignment.confidence_score, 0.0)


class TestErrorHandlingUX(unittest.TestCase):
    """Test user experience for error conditions"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False) 
        self.temp_file.close()
        
        # Reset singleton
        import src.agentic_orchestrator
        src.agentic_orchestrator._orchestrator = None
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_graceful_error_handling(self):
        """Test that errors are handled gracefully with user-friendly messages"""
        with capture_stdout() as output:
            result = simulate_task(
                description="Test task for error handling",
                task_type="auto",
                success_rate=0.0,  # Force failure
                duration=100.0
            )
        
        output_text = output.getvalue()
        
        # Should still provide meaningful output even on failure
        self.assertIn("Task assigned:", output_text)
        self.assertIn("Confidence:", output_text)
        
        # Result should indicate failure
        self.assertFalse(result["success"])
        self.assertLess(result["quality_score"], 0.8)
    
    def test_system_resilience(self):
        """Test system resilience under various conditions"""
        orchestrator = get_orchestrator()
        
        # Test with various edge case inputs
        edge_cases = [
            "",  # Empty description
            "a",  # Very short description
            "x" * 1000,  # Very long description
            "Design build review test security",  # Ambiguous classification
        ]
        
        for i, description in enumerate(edge_cases):
            from src.agentic_orchestrator import TaskRequest
            
            request = TaskRequest(
                description=description,
                context={"test": f"edge_case_{i}"},
                requester="test_user"
            )
            
            # Should handle all cases without crashing
            assignment = orchestrator.process_task_request(request)
            self.assertIsInstance(assignment, AgentAssignment)
            
            # Complete the task
            orchestrator.complete_task(
                task_id=assignment.task_id,
                success=True,
                execution_time=50.0,
                quality_score=0.7
            )


if __name__ == '__main__':
    unittest.main()