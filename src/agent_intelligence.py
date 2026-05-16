#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dynamic Agent Selection Intelligence Layer for Agentic Engineering

This module implements the dynamic routing intelligence that enhances the agentic 
engineering system by selecting the most appropriate agents for different tasks 
based on real-time decision-making factors.

Key Features:
- Task classification and routing
- Agent selection based on task type, security level, complexity, and history
- Outcome learning and feedback intelligence
- Engineering memory for organizational context
- Fallback mechanisms for reliability
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class TaskType(Enum):
    """Task classification types"""
    DESIGN = "design"
    BUILD = "build" 
    REVIEW = "review"
    TESTING = "testing"
    SECURITY = "security"
    DOCUMENTATION = "documentation"
    REFACTORING = "refactoring"


class SecurityLevel(Enum):
    """Security classification levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplexityLevel(Enum):
    """Task complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


class AgentType(Enum):
    """Available agent types"""
    CHATGPT_DESIGN = "chatgpt_design"
    CLAUDE_BUILD = "claude_build"
    GITHUB_COPILOT_REVIEW = "github_copilot_review"
    SPECIALIZED_SECURITY = "specialized_security"
    SPECIALIZED_TESTING = "specialized_testing"


@dataclass
class TaskContext:
    """Context information for a task"""
    task_id: str
    task_type: TaskType
    security_level: SecurityLevel
    complexity_level: ComplexityLevel
    description: str
    metadata: Dict[str, Any]
    timestamp: datetime


@dataclass
class AgentCapability:
    """Agent capability definition"""
    agent_type: AgentType
    supported_tasks: List[TaskType]
    security_clearance: SecurityLevel
    complexity_rating: ComplexityLevel
    performance_metrics: Dict[str, float]
    availability: bool = True


@dataclass
class OutcomeRecord:
    """Record of task execution outcome"""
    task_id: str
    agent_type: AgentType
    success: bool
    execution_time: float
    quality_score: float
    feedback: str
    timestamp: datetime
    error_count: int = 0
    retry_count: int = 0


class RoutingIntelligenceLayer:
    """
    Dynamic routing intelligence for agent selection.
    
    This class implements the core logic for selecting the most appropriate
    agent for a given task based on multiple factors and historical data.
    """
    
    def __init__(self, memory_file: str = "agent_memory.json"):
        self.memory_file = memory_file
        self.agents: Dict[AgentType, AgentCapability] = {}
        self.outcome_history: List[OutcomeRecord] = []
        self.task_history: Dict[str, TaskContext] = {}
        self.learning_enabled = True
        
        # Initialize default agents
        self._initialize_default_agents()
        
        # Load historical data
        self._load_memory()
    
    def _initialize_default_agents(self):
        """Initialize default agent capabilities based on STANDARDS.md"""
        
        # ChatGPT Design Agent (Rule 1)
        self.agents[AgentType.CHATGPT_DESIGN] = AgentCapability(
            agent_type=AgentType.CHATGPT_DESIGN,
            supported_tasks=[TaskType.DESIGN, TaskType.DOCUMENTATION],
            security_clearance=SecurityLevel.HIGH,
            complexity_rating=ComplexityLevel.EXPERT,
            performance_metrics={
                "success_rate": 0.95,
                "avg_execution_time": 300.0,
                "quality_score": 0.9
            }
        )
        
        # Claude Build Agent (Rule 2)
        self.agents[AgentType.CLAUDE_BUILD] = AgentCapability(
            agent_type=AgentType.CLAUDE_BUILD,
            supported_tasks=[TaskType.BUILD, TaskType.TESTING, TaskType.REFACTORING],
            security_clearance=SecurityLevel.HIGH,
            complexity_rating=ComplexityLevel.EXPERT,
            performance_metrics={
                "success_rate": 0.92,
                "avg_execution_time": 600.0,
                "quality_score": 0.88
            }
        )
        
        # GitHub Copilot Review Agent (Rule 3)
        self.agents[AgentType.GITHUB_COPILOT_REVIEW] = AgentCapability(
            agent_type=AgentType.GITHUB_COPILOT_REVIEW,
            supported_tasks=[TaskType.REVIEW, TaskType.SECURITY],
            security_clearance=SecurityLevel.CRITICAL,
            complexity_rating=ComplexityLevel.EXPERT,
            performance_metrics={
                "success_rate": 0.90,
                "avg_execution_time": 180.0,
                "quality_score": 0.85
            }
        )
        
        # Specialized Security Agent
        self.agents[AgentType.SPECIALIZED_SECURITY] = AgentCapability(
            agent_type=AgentType.SPECIALIZED_SECURITY,
            supported_tasks=[TaskType.SECURITY, TaskType.REVIEW],
            security_clearance=SecurityLevel.CRITICAL,
            complexity_rating=ComplexityLevel.EXPERT,
            performance_metrics={
                "success_rate": 0.88,
                "avg_execution_time": 240.0,
                "quality_score": 0.92
            }
        )
        
        # Specialized Testing Agent
        self.agents[AgentType.SPECIALIZED_TESTING] = AgentCapability(
            agent_type=AgentType.SPECIALIZED_TESTING,
            supported_tasks=[TaskType.TESTING, TaskType.BUILD],
            security_clearance=SecurityLevel.MEDIUM,
            complexity_rating=ComplexityLevel.COMPLEX,
            performance_metrics={
                "success_rate": 0.87,
                "avg_execution_time": 420.0,
                "quality_score": 0.83
            }
        )
    
    def select_agent(self, task_context: TaskContext) -> Tuple[AgentType, float]:
        """
        Select the most appropriate agent for a given task context.
        
        Args:
            task_context: Context information about the task
            
        Returns:
            Tuple of (selected_agent_type, confidence_score)
        """
        # Generate task signature for caching and learning
        task_signature = self._generate_task_signature(task_context)
        
        # Store task context
        self.task_history[task_context.task_id] = task_context
        
        # Get eligible agents
        eligible_agents = self._filter_eligible_agents(task_context)
        
        if not eligible_agents:
            # Fallback to default agent based on task type
            fallback_agent = self._get_fallback_agent(task_context.task_type)
            return fallback_agent, 0.5  # Low confidence for fallback
        
        # Score each eligible agent
        agent_scores = {}
        for agent_type in eligible_agents:
            score = self._calculate_agent_score(agent_type, task_context, task_signature)
            agent_scores[agent_type] = score
        
        # Select the highest scoring agent
        selected_agent = max(agent_scores.keys(), key=lambda x: agent_scores[x])
        confidence = agent_scores[selected_agent]
        
        return selected_agent, confidence
    
    def _filter_eligible_agents(self, task_context: TaskContext) -> List[AgentType]:
        """Filter agents that are eligible for the given task"""
        eligible = []
        
        for agent_type, capability in self.agents.items():
            # Check if agent is available
            if not capability.availability:
                continue
                
            # Check task type support
            if task_context.task_type not in capability.supported_tasks:
                continue
                
            # Check security clearance
            if self._security_level_value(capability.security_clearance) < \
               self._security_level_value(task_context.security_level):
                continue
                
            # Check complexity capability
            if self._complexity_level_value(capability.complexity_rating) < \
               self._complexity_level_value(task_context.complexity_level):
                continue
                
            eligible.append(agent_type)
        
        return eligible
    
    def _calculate_agent_score(self, agent_type: AgentType, task_context: TaskContext, 
                              task_signature: str) -> float:
        """Calculate a score for an agent based on multiple factors"""
        capability = self.agents[agent_type]
        score = 0.0
        
        # Base performance metrics (40% weight)
        base_score = (
            capability.performance_metrics.get("success_rate", 0.5) * 0.4 +
            capability.performance_metrics.get("quality_score", 0.5) * 0.3 +
            (1.0 - min(capability.performance_metrics.get("avg_execution_time", 600) / 1200.0, 1.0)) * 0.3
        )
        score += base_score * 0.4
        
        # Historical performance for similar tasks (30% weight)
        historical_score = self._get_historical_performance(agent_type, task_signature)
        score += historical_score * 0.3
        
        # Task type specialization bonus (20% weight)
        if task_context.task_type in capability.supported_tasks:
            specialization_index = capability.supported_tasks.index(task_context.task_type)
            # Higher bonus for primary specialization
            specialization_bonus = 1.0 - (specialization_index * 0.1)
            score += specialization_bonus * 0.2
        
        # Recent performance trend (10% weight)
        recent_trend = self._get_recent_performance_trend(agent_type)
        score += recent_trend * 0.1
        
        # Normalize score to [0, 1]
        return min(max(score, 0.0), 1.0)
    
    def _get_historical_performance(self, agent_type: AgentType, task_signature: str) -> float:
        """Get historical performance for similar tasks"""
        similar_outcomes = [
            outcome for outcome in self.outcome_history
            if outcome.agent_type == agent_type and 
            self._task_similarity(outcome.task_id, task_signature) > 0.7
        ]
        
        if not similar_outcomes:
            return 0.5  # Neutral score for no historical data
        
        # Weight recent outcomes more heavily
        total_weight = 0.0
        weighted_score = 0.0
        
        current_time = datetime.now()
        for outcome in similar_outcomes:
            # Exponential decay based on age (more recent = higher weight)
            days_old = (current_time - outcome.timestamp).days
            weight = 0.9 ** days_old  # Decay factor
            
            success_score = 1.0 if outcome.success else 0.0
            quality_factor = outcome.quality_score
            
            outcome_score = (success_score + quality_factor) / 2.0
            weighted_score += outcome_score * weight
            total_weight += weight
        
        return weighted_score / total_weight if total_weight > 0 else 0.5
    
    def _get_recent_performance_trend(self, agent_type: AgentType) -> float:
        """Get recent performance trend for the agent"""
        # Get outcomes from last 30 days
        cutoff_date = datetime.now() - timedelta(days=30)
        recent_outcomes = [
            outcome for outcome in self.outcome_history
            if outcome.agent_type == agent_type and outcome.timestamp > cutoff_date
        ]
        
        if len(recent_outcomes) < 3:
            return 0.5  # Not enough data for trend analysis
        
        # Sort by timestamp
        recent_outcomes.sort(key=lambda x: x.timestamp)
        
        # Calculate trend using linear regression on success rate
        success_scores = [1.0 if outcome.success else 0.0 for outcome in recent_outcomes]
        
        # Simple trend calculation
        first_half = success_scores[:len(success_scores)//2]
        second_half = success_scores[len(success_scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        # Convert trend to score
        trend_diff = second_avg - first_avg
        return 0.5 + (trend_diff * 0.5)  # Map [-1, 1] to [0, 1]
    
    def record_outcome(self, task_id: str, agent_type: AgentType, success: bool,
                      execution_time: float, quality_score: float, 
                      feedback: str = "", error_count: int = 0, retry_count: int = 0):
        """Record the outcome of a task execution for learning"""
        if not self.learning_enabled:
            return
            
        outcome = OutcomeRecord(
            task_id=task_id,
            agent_type=agent_type,
            success=success,
            execution_time=execution_time,
            quality_score=quality_score,
            feedback=feedback,
            timestamp=datetime.now(),
            error_count=error_count,
            retry_count=retry_count
        )
        
        self.outcome_history.append(outcome)
        
        # Update agent performance metrics
        self._update_agent_metrics(agent_type, outcome)
        
        # Save to persistent storage
        self._save_memory()
    
    def _update_agent_metrics(self, agent_type: AgentType, outcome: OutcomeRecord):
        """Update agent performance metrics based on outcome"""
        if agent_type not in self.agents:
            return
            
        agent = self.agents[agent_type]
        metrics = agent.performance_metrics
        
        # Get recent outcomes for this agent
        recent_outcomes = [
            o for o in self.outcome_history
            if o.agent_type == agent_type and 
            (datetime.now() - o.timestamp).days <= 90  # Last 90 days
        ]
        
        if recent_outcomes:
            # Recalculate metrics
            success_count = sum(1 for o in recent_outcomes if o.success)
            metrics["success_rate"] = success_count / len(recent_outcomes)
            
            metrics["avg_execution_time"] = sum(o.execution_time for o in recent_outcomes) / len(recent_outcomes)
            metrics["quality_score"] = sum(o.quality_score for o in recent_outcomes) / len(recent_outcomes)
    
    def _generate_task_signature(self, task_context: TaskContext) -> str:
        """Generate a signature for task similarity comparison"""
        # Create a hash based on task characteristics
        content = f"{task_context.task_type.value}_{task_context.security_level.value}_{task_context.complexity_level.value}"
        
        # Include key metadata
        for key in ["keywords", "domain", "component"]:
            if key in task_context.metadata:
                content += f"_{task_context.metadata[key]}"
        
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _task_similarity(self, task_id: str, task_signature: str) -> float:
        """Calculate similarity between tasks"""
        if task_id not in self.task_history:
            return 0.0
            
        task_context = self.task_history[task_id]
        other_signature = self._generate_task_signature(task_context)
        
        # Simple similarity based on signature match
        return 1.0 if task_signature == other_signature else 0.0
    
    def _get_fallback_agent(self, task_type: TaskType) -> AgentType:
        """Get fallback agent for a task type based on STANDARDS.md rules"""
        fallback_mapping = {
            TaskType.DESIGN: AgentType.CHATGPT_DESIGN,
            TaskType.BUILD: AgentType.CLAUDE_BUILD,
            TaskType.REVIEW: AgentType.GITHUB_COPILOT_REVIEW,
            TaskType.TESTING: AgentType.CLAUDE_BUILD,
            TaskType.SECURITY: AgentType.GITHUB_COPILOT_REVIEW,
            TaskType.DOCUMENTATION: AgentType.CHATGPT_DESIGN,
            TaskType.REFACTORING: AgentType.CLAUDE_BUILD,
        }
        
        return fallback_mapping.get(task_type, AgentType.CLAUDE_BUILD)
    
    def _security_level_value(self, level: SecurityLevel) -> int:
        """Convert security level to numeric value for comparison"""
        mapping = {
            SecurityLevel.LOW: 1,
            SecurityLevel.MEDIUM: 2,
            SecurityLevel.HIGH: 3,
            SecurityLevel.CRITICAL: 4
        }
        return mapping[level]
    
    def _complexity_level_value(self, level: ComplexityLevel) -> int:
        """Convert complexity level to numeric value for comparison"""
        mapping = {
            ComplexityLevel.SIMPLE: 1,
            ComplexityLevel.MODERATE: 2,
            ComplexityLevel.COMPLEX: 3,
            ComplexityLevel.EXPERT: 4
        }
        return mapping[level]
    
    def _load_memory(self):
        """Load historical data from persistent storage"""
        try:
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
                
            # Load outcome history
            for outcome_data in data.get('outcomes', []):
                outcome = OutcomeRecord(
                    task_id=outcome_data['task_id'],
                    agent_type=AgentType(outcome_data['agent_type']),
                    success=outcome_data['success'],
                    execution_time=outcome_data['execution_time'],
                    quality_score=outcome_data['quality_score'],
                    feedback=outcome_data['feedback'],
                    timestamp=datetime.fromisoformat(outcome_data['timestamp']),
                    error_count=outcome_data.get('error_count', 0),
                    retry_count=outcome_data.get('retry_count', 0)
                )
                self.outcome_history.append(outcome)
                
            # Load task history
            for task_id, task_data in data.get('tasks', {}).items():
                task_context = TaskContext(
                    task_id=task_data['task_id'],
                    task_type=TaskType(task_data['task_type']),
                    security_level=SecurityLevel(task_data['security_level']),
                    complexity_level=ComplexityLevel(task_data['complexity_level']),
                    description=task_data['description'],
                    metadata=task_data['metadata'],
                    timestamp=datetime.fromisoformat(task_data['timestamp'])
                )
                self.task_history[task_id] = task_context
                
        except FileNotFoundError:
            # First run - no historical data
            pass
        except Exception as e:
            print(f"Warning: Failed to load agent memory: {e}")
    
    def _save_memory(self):
        """Save historical data to persistent storage"""
        try:
            data = {
                'outcomes': [
                    {
                        'task_id': outcome.task_id,
                        'agent_type': outcome.agent_type.value,
                        'success': outcome.success,
                        'execution_time': outcome.execution_time,
                        'quality_score': outcome.quality_score,
                        'feedback': outcome.feedback,
                        'timestamp': outcome.timestamp.isoformat(),
                        'error_count': outcome.error_count,
                        'retry_count': outcome.retry_count
                    }
                    for outcome in self.outcome_history[-1000:]  # Keep last 1000 outcomes
                ],
                'tasks': {
                    task_id: {
                        'task_id': task.task_id,
                        'task_type': task.task_type.value,
                        'security_level': task.security_level.value,
                        'complexity_level': task.complexity_level.value,
                        'description': task.description,
                        'metadata': task.metadata,
                        'timestamp': task.timestamp.isoformat()
                    }
                    for task_id, task in list(self.task_history.items())[-500:]  # Keep last 500 tasks
                }
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Failed to save agent memory: {e}")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all agents and system performance"""
        status = {
            'agents': {},
            'system_metrics': {
                'total_tasks': len(self.task_history),
                'total_outcomes': len(self.outcome_history),
                'overall_success_rate': 0.0,
                'avg_execution_time': 0.0
            }
        }
        
        # Agent status
        for agent_type, capability in self.agents.items():
            recent_outcomes = [
                o for o in self.outcome_history
                if o.agent_type == agent_type and 
                (datetime.now() - o.timestamp).days <= 30
            ]
            
            status['agents'][agent_type.value] = {
                'availability': capability.availability,
                'performance_metrics': capability.performance_metrics,
                'recent_tasks': len(recent_outcomes),
                'recent_success_rate': sum(1 for o in recent_outcomes if o.success) / len(recent_outcomes) if recent_outcomes else 0.0
            }
        
        # System metrics
        if self.outcome_history:
            successful_outcomes = sum(1 for o in self.outcome_history if o.success)
            status['system_metrics']['overall_success_rate'] = successful_outcomes / len(self.outcome_history)
            status['system_metrics']['avg_execution_time'] = sum(o.execution_time for o in self.outcome_history) / len(self.outcome_history)
        
        return status


# Singleton instance for global access
_routing_intelligence = None

def get_routing_intelligence() -> RoutingIntelligenceLayer:
    """Get the global routing intelligence instance"""
    global _routing_intelligence
    if _routing_intelligence is None:
        _routing_intelligence = RoutingIntelligenceLayer()
    return _routing_intelligence


def classify_task(description: str, metadata: Dict[str, Any] = None) -> Tuple[TaskType, SecurityLevel, ComplexityLevel]:
    """
    Classify a task based on its description and metadata.
    
    This is a simple classifier - in production, this could use ML models.
    """
    if metadata is None:
        metadata = {}
    
    description_lower = description.lower()
    
    # Task type classification
    task_type = TaskType.BUILD  # Default
    
    if any(keyword in description_lower for keyword in ["design", "architect", "plan", "specification"]):
        task_type = TaskType.DESIGN
    elif any(keyword in description_lower for keyword in ["review", "check", "validate", "audit"]):
        task_type = TaskType.REVIEW
    elif any(keyword in description_lower for keyword in ["test", "verify", "quality"]):
        task_type = TaskType.TESTING
    elif any(keyword in description_lower for keyword in ["security", "vulnerability", "auth", "encryption"]):
        task_type = TaskType.SECURITY
    elif any(keyword in description_lower for keyword in ["document", "readme", "guide"]):
        task_type = TaskType.DOCUMENTATION
    elif any(keyword in description_lower for keyword in ["refactor", "cleanup", "optimize"]):
        task_type = TaskType.REFACTORING
    
    # Security level classification
    security_level = SecurityLevel.MEDIUM  # Default
    
    if any(keyword in description_lower for keyword in ["public", "open source", "demo"]):
        security_level = SecurityLevel.LOW
    elif any(keyword in description_lower for keyword in ["internal", "private", "confidential"]):
        security_level = SecurityLevel.HIGH
    elif any(keyword in description_lower for keyword in ["secret", "critical", "production", "auth", "security"]):
        security_level = SecurityLevel.CRITICAL
    
    # Complexity level classification
    complexity_level = ComplexityLevel.MODERATE  # Default
    
    if any(keyword in description_lower for keyword in ["simple", "basic", "quick", "minor"]):
        complexity_level = ComplexityLevel.SIMPLE
    elif any(keyword in description_lower for keyword in ["complex", "advanced", "enterprise", "scale"]):
        complexity_level = ComplexityLevel.COMPLEX
    elif any(keyword in description_lower for keyword in ["expert", "critical", "performance", "optimization"]):
        complexity_level = ComplexityLevel.EXPERT
    
    return task_type, security_level, complexity_level