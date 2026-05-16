#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agentic Engineering Orchestrator

This module provides the integration layer between the dynamic agent selection
intelligence and the existing agentic engineering workflow defined in STANDARDS.md.

It replaces static agent assignment with intelligent routing while maintaining
backward compatibility with existing workflows.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

from agent_intelligence import (
    get_routing_intelligence, classify_task,
    TaskContext, TaskType, SecurityLevel, ComplexityLevel,
    AgentType
)


@dataclass
class TaskRequest:
    """Request for task execution through agentic orchestration"""
    description: str
    context: Dict[str, Any]
    requester: str
    priority: str = "medium"
    deadline: Optional[datetime] = None


@dataclass 
class AgentAssignment:
    """Result of agent assignment"""
    task_id: str
    assigned_agent: AgentType
    confidence_score: float
    fallback_agents: list
    reasoning: str
    estimated_duration: float


class AgenticOrchestrator:
    """
    Main orchestrator for the enhanced agentic engineering system.
    
    Integrates with existing STANDARDS.md workflow:
    - Rule 1: Design (ChatGPT) - enhanced with dynamic selection
    - Rule 2: Build (Claude) - enhanced with task-specific routing  
    - Rule 3: Review (GitHub Copilot) - enhanced with specialized agents
    """
    
    def __init__(self):
        self.intelligence_layer = get_routing_intelligence()
        self.active_tasks: Dict[str, TaskContext] = {}
        self.agent_assignments: Dict[str, AgentAssignment] = {}
    
    def process_task_request(self, request: TaskRequest) -> AgentAssignment:
        """
        Process a new task request and assign the most appropriate agent.
        
        Args:
            request: Task request details
            
        Returns:
            Agent assignment with reasoning and alternatives
        """
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Classify the task
        task_type, security_level, complexity_level = classify_task(
            request.description, 
            request.context
        )
        
        # Create task context
        task_context = TaskContext(
            task_id=task_id,
            task_type=task_type,
            security_level=security_level,
            complexity_level=complexity_level,
            description=request.description,
            metadata={
                **request.context,
                "requester": request.requester,
                "priority": request.priority,
                "deadline": request.deadline.isoformat() if request.deadline else None
            },
            timestamp=datetime.now()
        )
        
        # Select primary agent
        assigned_agent, confidence = self.intelligence_layer.select_agent(task_context)
        
        # Generate fallback options
        fallback_agents = self._get_fallback_options(task_context, assigned_agent)
        
        # Estimate execution duration
        estimated_duration = self._estimate_duration(assigned_agent, task_context)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(task_context, assigned_agent, confidence)
        
        # Create assignment
        assignment = AgentAssignment(
            task_id=task_id,
            assigned_agent=assigned_agent,
            confidence_score=confidence,
            fallback_agents=fallback_agents,
            reasoning=reasoning,
            estimated_duration=estimated_duration
        )
        
        # Store for tracking
        self.active_tasks[task_id] = task_context
        self.agent_assignments[task_id] = assignment
        
        return assignment
    
    def complete_task(self, task_id: str, success: bool, execution_time: float,
                     quality_score: float, feedback: str = "", 
                     error_count: int = 0, retry_count: int = 0):
        """
        Record task completion for learning and metrics.
        
        Args:
            task_id: Task identifier
            success: Whether task completed successfully
            execution_time: Actual execution time in seconds
            quality_score: Quality assessment (0.0 to 1.0)
            feedback: Optional feedback or error details
            error_count: Number of errors encountered
            retry_count: Number of retries required
        """
        if task_id not in self.agent_assignments:
            return
            
        assignment = self.agent_assignments[task_id]
        
        # Record outcome for learning
        self.intelligence_layer.record_outcome(
            task_id=task_id,
            agent_type=assignment.assigned_agent,
            success=success,
            execution_time=execution_time,
            quality_score=quality_score,
            feedback=feedback,
            error_count=error_count,
            retry_count=retry_count
        )
        
        # Clean up completed task
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
        if task_id in self.agent_assignments:
            del self.agent_assignments[task_id]
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status information for a task"""
        if task_id not in self.active_tasks:
            return {"error": "Task not found"}
            
        task_context = self.active_tasks[task_id]
        assignment = self.agent_assignments.get(task_id)
        
        return {
            "task_id": task_id,
            "description": task_context.description,
            "task_type": task_context.task_type.value,
            "security_level": task_context.security_level.value,
            "complexity_level": task_context.complexity_level.value,
            "assigned_agent": assignment.assigned_agent.value if assignment else None,
            "confidence_score": assignment.confidence_score if assignment else None,
            "estimated_duration": assignment.estimated_duration if assignment else None,
            "start_time": task_context.timestamp.isoformat(),
            "status": "in_progress"
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status and metrics"""
        base_status = self.intelligence_layer.get_agent_status()
        
        base_status.update({
            "active_tasks": len(self.active_tasks),
            "orchestrator_version": "1.0",
            "intelligence_enabled": True,
            "learning_enabled": self.intelligence_layer.learning_enabled
        })
        
        return base_status
    
    def _get_fallback_options(self, task_context: TaskContext, 
                             primary_agent: AgentType) -> list:
        """Generate fallback agent options"""
        fallbacks = []
        
        # Get all agents that could handle this task type
        for agent_type, capability in self.intelligence_layer.agents.items():
            if (agent_type != primary_agent and 
                task_context.task_type in capability.supported_tasks and
                capability.availability):
                
                fallbacks.append(agent_type.value)
        
        # Sort by performance metrics
        fallbacks.sort(key=lambda agent_name: 
                      self.intelligence_layer.agents[AgentType(agent_name)].performance_metrics.get("success_rate", 0.0),
                      reverse=True)
        
        return fallbacks[:3]  # Return top 3 fallbacks
    
    def _estimate_duration(self, agent_type: AgentType, task_context: TaskContext) -> float:
        """Estimate task execution duration"""
        if agent_type not in self.intelligence_layer.agents:
            return 600.0  # Default 10 minutes
            
        capability = self.intelligence_layer.agents[agent_type]
        base_time = capability.performance_metrics.get("avg_execution_time", 600.0)
        
        # Adjust for complexity
        complexity_multiplier = {
            ComplexityLevel.SIMPLE: 0.5,
            ComplexityLevel.MODERATE: 1.0,
            ComplexityLevel.COMPLEX: 1.8,
            ComplexityLevel.EXPERT: 3.0
        }
        
        multiplier = complexity_multiplier.get(task_context.complexity_level, 1.0)
        return base_time * multiplier
    
    def _generate_reasoning(self, task_context: TaskContext, 
                          assigned_agent: AgentType, confidence: float) -> str:
        """Generate human-readable reasoning for agent selection"""
        reasoning_parts = []
        
        # Task classification reasoning
        reasoning_parts.append(
            f"Task classified as {task_context.task_type.value} "
            f"with {task_context.security_level.value} security and "
            f"{task_context.complexity_level.value} complexity."
        )
        
        # Agent selection reasoning
        if assigned_agent == AgentType.CHATGPT_DESIGN:
            reasoning_parts.append("Selected ChatGPT Design Agent for architectural planning and design tasks.")
        elif assigned_agent == AgentType.CLAUDE_BUILD:
            reasoning_parts.append("Selected Claude Build Agent for implementation, testing, and development tasks.")
        elif assigned_agent == AgentType.GITHUB_COPILOT_REVIEW:
            reasoning_parts.append("Selected GitHub Copilot for code review and security analysis.")
        elif assigned_agent == AgentType.SPECIALIZED_SECURITY:
            reasoning_parts.append("Selected Specialized Security Agent for enhanced security analysis.")
        elif assigned_agent == AgentType.SPECIALIZED_TESTING:
            reasoning_parts.append("Selected Specialized Testing Agent for comprehensive test coverage.")
        
        # Confidence reasoning
        if confidence >= 0.8:
            reasoning_parts.append("High confidence selection based on strong historical performance and exact capability match.")
        elif confidence >= 0.6:
            reasoning_parts.append("Good confidence selection with favorable historical data and capability alignment.")
        else:
            reasoning_parts.append("Moderate confidence selection - may benefit from human oversight or fallback options.")
        
        return " ".join(reasoning_parts)


# Singleton instance
_orchestrator = None

def get_orchestrator() -> AgenticOrchestrator:
    """Get the global orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgenticOrchestrator()
    return _orchestrator


# Integration functions for existing workflow compatibility
def assign_design_task(description: str, context: Dict[str, Any] = None, 
                      requester: str = "system") -> AgentAssignment:
    """Assign a design task using intelligent routing"""
    if context is None:
        context = {}
        
    context["task_hint"] = "design"  # Hint for classification
    
    request = TaskRequest(
        description=description,
        context=context,
        requester=requester
    )
    
    return get_orchestrator().process_task_request(request)


def assign_build_task(description: str, context: Dict[str, Any] = None,
                     requester: str = "system") -> AgentAssignment:
    """Assign a build task using intelligent routing"""  
    if context is None:
        context = {}
        
    context["task_hint"] = "build"  # Hint for classification
    
    request = TaskRequest(
        description=description,
        context=context,
        requester=requester
    )
    
    return get_orchestrator().process_task_request(request)


def assign_review_task(description: str, context: Dict[str, Any] = None,
                      requester: str = "system") -> AgentAssignment:
    """Assign a review task using intelligent routing"""
    if context is None:
        context = {}
        
    context["task_hint"] = "review"  # Hint for classification
    
    request = TaskRequest(
        description=description,
        context=context,
        requester=requester
    )
    
    return get_orchestrator().process_task_request(request)


def record_task_completion(task_id: str, success: bool, execution_time: float,
                          quality_score: float, feedback: str = ""):
    """Record task completion for any task type"""
    get_orchestrator().complete_task(
        task_id=task_id,
        success=success,
        execution_time=execution_time,
        quality_score=quality_score,
        feedback=feedback
    )