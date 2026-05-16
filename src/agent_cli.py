#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Selection CLI Tool

Command-line interface for testing and demonstrating the dynamic agent
selection intelligence layer. Provides utilities for task simulation,
system monitoring, and performance analysis.
"""

import argparse
import json
import sys
import time
from datetime import datetime
from typing import Dict, Any

from agentic_orchestrator import (
    get_orchestrator, assign_design_task, assign_build_task, 
    assign_review_task, record_task_completion
)
from agent_intelligence import (
    TaskType, SecurityLevel, ComplexityLevel, AgentType
)


def simulate_task(description: str, task_type: str = "auto", 
                 success_rate: float = 0.9, duration: float = 300.0) -> Dict[str, Any]:
    """
    Simulate a task execution for testing the intelligence layer.
    
    Args:
        description: Task description
        task_type: Task type hint (design/build/review/auto)
        success_rate: Probability of success (for simulation)
        duration: Simulated execution time
        
    Returns:
        Task execution results
    """
    # Assign the task
    if task_type == "design":
        assignment = assign_design_task(description, {"simulation": True})
    elif task_type == "build":
        assignment = assign_build_task(description, {"simulation": True})
    elif task_type == "review":
        assignment = assign_review_task(description, {"simulation": True})
    else:
        # Auto-assign based on description
        orchestrator = get_orchestrator()
        from agentic_orchestrator import TaskRequest
        request = TaskRequest(
            description=description,
            context={"simulation": True},
            requester="cli_simulation"
        )
        assignment = orchestrator.process_task_request(request)
    
    print(f"Task assigned: {assignment.assigned_agent.value}")
    print(f"Confidence: {assignment.confidence_score:.2f}")
    print(f"Reasoning: {assignment.reasoning}")
    print(f"Estimated duration: {assignment.estimated_duration:.1f}s")
    
    # Simulate execution
    import random
    time.sleep(0.1)  # Brief pause for realism
    
    actual_duration = duration + random.uniform(-60, 60)  # Add some variance
    success = random.random() < success_rate
    quality_score = random.uniform(0.7, 0.95) if success else random.uniform(0.3, 0.7)
    
    # Record the outcome
    feedback = "Task completed successfully" if success else "Task encountered issues"
    record_task_completion(
        task_id=assignment.task_id,
        success=success,
        execution_time=actual_duration,
        quality_score=quality_score,
        feedback=feedback
    )
    
    return {
        "task_id": assignment.task_id,
        "assigned_agent": assignment.assigned_agent.value,
        "confidence": assignment.confidence_score,
        "success": success,
        "execution_time": actual_duration,
        "quality_score": quality_score
    }


def run_batch_simulation(count: int = 10, task_types: list = None):
    """Run a batch of simulated tasks for testing"""
    if task_types is None:
        task_types = ["design", "build", "review"]
    
    task_templates = {
        "design": [
            "Design user authentication system",
            "Plan database architecture for user management",
            "Design REST API for mobile app",
            "Create system architecture for microservices",
            "Plan security model for enterprise application"
        ],
        "build": [
            "Implement user registration functionality",
            "Build JWT authentication middleware", 
            "Create unit tests for user service",
            "Develop API endpoints for data access",
            "Build CI/CD pipeline configuration"
        ],
        "review": [
            "Review security of authentication code",
            "Audit database access patterns",
            "Check API security vulnerabilities", 
            "Validate test coverage and quality",
            "Review code for performance issues"
        ]
    }
    
    results = []
    
    print(f"Running batch simulation with {count} tasks...")
    print("-" * 50)
    
    import random
    for i in range(count):
        task_type = random.choice(task_types)
        description = random.choice(task_templates[task_type])
        
        print(f"\nTask {i+1}: {description}")
        result = simulate_task(description, task_type)
        results.append(result)
    
    # Summary
    print("\n" + "="*50)
    print("SIMULATION SUMMARY")
    print("="*50)
    
    success_count = sum(1 for r in results if r["success"])
    avg_confidence = sum(r["confidence"] for r in results) / len(results)
    avg_quality = sum(r["quality_score"] for r in results) / len(results)
    
    agent_usage = {}
    for r in results:
        agent = r["assigned_agent"]
        agent_usage[agent] = agent_usage.get(agent, 0) + 1
    
    print(f"Success Rate: {success_count}/{count} ({success_count/count*100:.1f}%)")
    print(f"Average Confidence: {avg_confidence:.2f}")
    print(f"Average Quality: {avg_quality:.2f}")
    print(f"\nAgent Usage:")
    for agent, usage in sorted(agent_usage.items()):
        print(f"  {agent}: {usage} tasks ({usage/count*100:.1f}%)")


def show_system_status():
    """Display current system status and metrics"""
    orchestrator = get_orchestrator()
    status = orchestrator.get_system_status()
    
    print("AGENTIC ENGINEERING SYSTEM STATUS")
    print("="*50)
    print(f"Orchestrator Version: {status['orchestrator_version']}")
    print(f"Intelligence Enabled: {status['intelligence_enabled']}")
    print(f"Learning Enabled: {status['learning_enabled']}")
    print(f"Active Tasks: {status['active_tasks']}")
    
    print(f"\nSYSTEM METRICS")
    print("-" * 30)
    metrics = status['system_metrics']
    print(f"Total Tasks Processed: {metrics['total_tasks']}")
    print(f"Total Outcomes Recorded: {metrics['total_outcomes']}")
    print(f"Overall Success Rate: {metrics['overall_success_rate']:.2%}")
    print(f"Average Execution Time: {metrics['avg_execution_time']:.1f}s")
    
    print(f"\nAGENT STATUS")
    print("-" * 30)
    for agent_name, agent_info in status['agents'].items():
        print(f"\n{agent_name.upper()}:")
        print(f"  Available: {agent_info['availability']}")
        print(f"  Success Rate: {agent_info['performance_metrics']['success_rate']:.2%}")
        print(f"  Avg Quality: {agent_info['performance_metrics']['quality_score']:.2f}")
        print(f"  Avg Duration: {agent_info['performance_metrics']['avg_execution_time']:.1f}s")
        print(f"  Recent Tasks: {agent_info['recent_tasks']}")
        print(f"  Recent Success: {agent_info['recent_success_rate']:.2%}")


def interactive_mode():
    """Run in interactive mode for manual testing"""
    print("INTERACTIVE AGENT SELECTION MODE")
    print("="*40)
    print("Enter task descriptions to see agent assignments.")
    print("Commands: 'status', 'quit', or describe a task")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            elif user_input.lower() == 'status':
                show_system_status()
                continue
                
            elif not user_input:
                continue
            
            # Process as task description
            print(f"\nAnalyzing: '{user_input}'")
            result = simulate_task(user_input, duration=0.1)  # Quick simulation
            
            print(f"✓ Simulated execution: {'Success' if result['success'] else 'Failed'}")
            print(f"  Quality Score: {result['quality_score']:.2f}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Dynamic Agent Selection Intelligence CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent_cli.py status                    # Show system status
  python agent_cli.py simulate "Build API"     # Simulate single task  
  python agent_cli.py batch 20                 # Run batch simulation
  python agent_cli.py interactive              # Interactive mode
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    
    # Simulate command
    sim_parser = subparsers.add_parser('simulate', help='Simulate a single task')
    sim_parser.add_argument('description', help='Task description')
    sim_parser.add_argument('--type', choices=['design', 'build', 'review', 'auto'], 
                           default='auto', help='Task type hint')
    sim_parser.add_argument('--success-rate', type=float, default=0.9,
                           help='Success probability (0.0-1.0)')
    sim_parser.add_argument('--duration', type=float, default=300.0,
                           help='Simulated duration in seconds')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Run batch simulation')
    batch_parser.add_argument('count', type=int, help='Number of tasks to simulate')
    batch_parser.add_argument('--types', nargs='+', 
                             choices=['design', 'build', 'review'],
                             default=['design', 'build', 'review'],
                             help='Task types to include')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Interactive mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'status':
            show_system_status()
            
        elif args.command == 'simulate':
            result = simulate_task(
                args.description,
                args.type,
                args.success_rate,
                args.duration
            )
            print(f"\nResult: {json.dumps(result, indent=2, default=str)}")
            
        elif args.command == 'batch':
            run_batch_simulation(args.count, args.types)
            
        elif args.command == 'interactive':
            interactive_mode()
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()