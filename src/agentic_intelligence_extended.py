#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extended Agentic Intelligence Layers
===================================

Implements the remaining intelligence layers (8-13) for the Agentic Engineering System:
8. Cost-awareness Orchestration Engine
9. Reliability/SLO Framework for AI Agents  
10. Human Collaboration Intelligence
11. Compliance & Audit Intelligence
12. Benchmarkable Metrics System
13. Developer Trust & Adoption Strategy

These layers complete the transformation into a truly unique and defensible platform.
"""

import json
import time
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
from datetime import datetime, timedelta


# ═══════════════════════════════════════════════════════════════════════════════
# 8. COST-AWARENESS ORCHESTRATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CostProfile:
    """Cost profile for different AI agents and operations"""
    agent_type: str
    cost_per_token: float
    cost_per_minute: float
    estimated_tokens: int
    estimated_duration: float
    total_estimated_cost: float

@dataclass
class CostBudget:
    """Project cost budget and constraints"""
    monthly_budget: float
    current_spend: float
    cost_per_change_limit: float
    emergency_budget_reserve: float

class CostAwarenessEngine:
    """AI FinOps for engineering delivery - cost as first-class orchestration"""
    
    def __init__(self):
        self.cost_db_path = "cost_tracking.db"
        self._init_cost_database()
        self.agent_cost_profiles = self._load_agent_cost_profiles()
    
    def _init_cost_database(self):
        """Initialize cost tracking database"""
        conn = sqlite3.connect(self.cost_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cost_tracking (
            operation_id TEXT PRIMARY KEY,
            agent_type TEXT,
            operation_type TEXT,
            actual_cost REAL,
            estimated_cost REAL,
            tokens_used INTEGER,
            duration_minutes REAL,
            timestamp REAL,
            repository TEXT,
            change_complexity INTEGER
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget_alerts (
            alert_id TEXT PRIMARY KEY,
            alert_type TEXT,
            budget_type TEXT,
            threshold_percentage REAL,
            triggered_at REAL,
            current_spend REAL,
            budget_limit REAL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def _load_agent_cost_profiles(self) -> Dict[str, Dict[str, float]]:
        """Load cost profiles for different AI agents"""
        return {
            "chatgpt-design": {
                "cost_per_1k_tokens": 0.03,
                "avg_tokens_per_design": 2000,
                "avg_duration_minutes": 5
            },
            "claude-build": {
                "cost_per_1k_tokens": 0.25,  # Higher for complex reasoning
                "avg_tokens_per_build": 5000,
                "avg_duration_minutes": 10
            },
            "copilot-review": {
                "cost_per_1k_tokens": 0.01,  # Covered by GitHub subscription
                "avg_tokens_per_review": 1500,
                "avg_duration_minutes": 3
            },
            "security-specialized": {
                "cost_per_1k_tokens": 0.35,  # Premium for security expertise
                "avg_tokens_per_operation": 3000,
                "avg_duration_minutes": 15
            },
            "lightweight-cheap": {
                "cost_per_1k_tokens": 0.002,  # Optimized for cost
                "avg_tokens_per_operation": 500,
                "avg_duration_minutes": 2
            }
        }
    
    def estimate_operation_cost(self, agent_type: str, complexity_score: int) -> CostProfile:
        """Estimate cost for a specific operation"""
        
        if agent_type not in self.agent_cost_profiles:
            agent_type = "claude-build"  # Default
            
        profile = self.agent_cost_profiles[agent_type]
        
        # Adjust estimates based on complexity
        complexity_multiplier = max(0.5, min(2.0, complexity_score / 5.0))
        
        estimated_tokens = int(profile.get("avg_tokens_per_operation", 
                                         profile.get("avg_tokens_per_design",
                                                   profile.get("avg_tokens_per_build", 1000))) * complexity_multiplier)
        
        estimated_duration = profile.get("avg_duration_minutes", 5) * complexity_multiplier
        
        cost_per_token = profile["cost_per_1k_tokens"] / 1000
        total_cost = estimated_tokens * cost_per_token
        
        return CostProfile(
            agent_type=agent_type,
            cost_per_token=cost_per_token,
            cost_per_minute=total_cost / estimated_duration if estimated_duration > 0 else 0,
            estimated_tokens=estimated_tokens,
            estimated_duration=estimated_duration,
            total_estimated_cost=total_cost
        )
    
    def optimize_for_budget(self, 
                          original_agent: str, 
                          cost_budget: CostBudget, 
                          complexity_score: int) -> str:
        """Optimize agent selection based on budget constraints"""
        
        original_cost = self.estimate_operation_cost(original_agent, complexity_score)
        
        # If within budget, use original selection
        if original_cost.total_estimated_cost <= cost_budget.cost_per_change_limit:
            return original_agent
        
        # Try cheaper alternatives
        cost_optimized_agents = [
            "lightweight-cheap",
            "copilot-review", 
            "chatgpt-design",
            "claude-build"
        ]
        
        for agent in cost_optimized_agents:
            cost = self.estimate_operation_cost(agent, complexity_score)
            if cost.total_estimated_cost <= cost_budget.cost_per_change_limit:
                return agent
        
        # If no agent fits budget, use cheapest with budget alert
        self._trigger_budget_alert("cost_per_change_exceeded", cost_budget)
        return "lightweight-cheap"
    
    def track_actual_cost(self, 
                         operation_id: str,
                         agent_type: str, 
                         actual_cost: float,
                         tokens_used: int,
                         duration_minutes: float):
        """Track actual costs for future optimization"""
        
        conn = sqlite3.connect(self.cost_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO cost_tracking 
        (operation_id, agent_type, operation_type, actual_cost, tokens_used, duration_minutes, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (operation_id, agent_type, "engineering_operation", actual_cost, tokens_used, duration_minutes, time.time()))
        
        conn.commit()
        conn.close()
    
    def get_roi_analytics(self, time_period_days: int = 30) -> Dict[str, Any]:
        """Generate ROI analytics for engineering delivery"""
        
        conn = sqlite3.connect(self.cost_db_path)
        cursor = conn.cursor()
        
        cutoff_time = time.time() - (time_period_days * 24 * 60 * 60)
        
        cursor.execute("""
        SELECT agent_type, COUNT(*), SUM(actual_cost), AVG(actual_cost)
        FROM cost_tracking
        WHERE timestamp >= ?
        GROUP BY agent_type
        """, (cutoff_time,))
        
        results = cursor.fetchall()
        conn.close()
        
        analytics = {
            "period_days": time_period_days,
            "agent_performance": {},
            "total_spend": 0,
            "total_operations": 0
        }
        
        for agent_type, count, total_cost, avg_cost in results:
            analytics["agent_performance"][agent_type] = {
                "operations_count": count,
                "total_cost": total_cost,
                "average_cost": avg_cost,
                "cost_efficiency_score": count / total_cost if total_cost > 0 else 0
            }
            analytics["total_spend"] += total_cost
            analytics["total_operations"] += count
        
        return analytics
    
    def _trigger_budget_alert(self, alert_type: str, budget: CostBudget):
        """Trigger budget alert for monitoring"""
        conn = sqlite3.connect(self.cost_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO budget_alerts
        (alert_id, alert_type, budget_type, current_spend, budget_limit, triggered_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (f"{alert_type}_{int(time.time())}", alert_type, "monthly", 
              budget.current_spend, budget.monthly_budget, time.time()))
        
        conn.commit()
        conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# 9. RELIABILITY/SLO FRAMEWORK FOR AI AGENTS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ServiceLevelObjective:
    """SLO definition for AI agent reliability"""
    slo_name: str
    target_percentage: float  # e.g., 99.9
    measurement_window_hours: int
    error_budget_percentage: float

@dataclass
class AgentReliabilityMetrics:
    """Reliability metrics for AI agents"""
    agent_type: str
    success_rate: float
    average_latency_ms: float
    error_rate: float
    availability: float
    mean_time_to_recovery: float

class ReliabilityFramework:
    """Enterprise-grade reliability engineering for AI agents"""
    
    def __init__(self):
        self.reliability_db = "agent_reliability.db"
        self._init_reliability_database()
        self.slos = self._define_service_level_objectives()
        
    def _init_reliability_database(self):
        """Initialize reliability tracking database"""
        conn = sqlite3.connect(self.reliability_db)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_operations (
            operation_id TEXT PRIMARY KEY,
            agent_type TEXT,
            operation_type TEXT,
            start_time REAL,
            end_time REAL,
            success BOOLEAN,
            error_type TEXT,
            latency_ms REAL,
            retry_count INTEGER,
            fallback_used BOOLEAN
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS circuit_breaker_events (
            event_id TEXT PRIMARY KEY,
            agent_type TEXT,
            event_type TEXT,  -- 'open', 'close', 'half_open'
            timestamp REAL,
            error_rate REAL,
            consecutive_failures INTEGER
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS slo_violations (
            violation_id TEXT PRIMARY KEY,
            slo_name TEXT,
            agent_type TEXT,
            violation_type TEXT,
            actual_value REAL,
            target_value REAL,
            timestamp REAL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def _define_service_level_objectives(self) -> Dict[str, ServiceLevelObjective]:
        """Define SLOs for different AI agents"""
        return {
            "claude-build": ServiceLevelObjective(
                slo_name="claude_build_reliability",
                target_percentage=99.5,
                measurement_window_hours=24,
                error_budget_percentage=0.5
            ),
            "copilot-review": ServiceLevelObjective(
                slo_name="copilot_review_availability", 
                target_percentage=99.9,
                measurement_window_hours=24,
                error_budget_percentage=0.1
            ),
            "security-specialized": ServiceLevelObjective(
                slo_name="security_agent_accuracy",
                target_percentage=99.8,
                measurement_window_hours=168,  # Weekly measurement
                error_budget_percentage=0.2
            )
        }
    
    def record_agent_operation(self, 
                              operation_id: str,
                              agent_type: str,
                              operation_type: str,
                              success: bool,
                              latency_ms: float,
                              error_type: Optional[str] = None,
                              retry_count: int = 0,
                              fallback_used: bool = False):
        """Record agent operation for reliability tracking"""
        
        conn = sqlite3.connect(self.reliability_db)
        try:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR IGNORE INTO agent_operations
            (operation_id, agent_type, operation_type, start_time, end_time, success,
             error_type, latency_ms, retry_count, fallback_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (operation_id, agent_type, operation_type, time.time() - latency_ms/1000,
                  time.time(), success, error_type, latency_ms, retry_count, fallback_used))
            conn.commit()
        finally:
            conn.close()

        # Check SLO compliance
        self._check_slo_compliance(agent_type)
    
    def _check_slo_compliance(self, agent_type: str):
        """Check if agent is meeting SLO targets"""
        
        if agent_type not in self.slos:
            return
        
        slo = self.slos[agent_type]
        window_start = time.time() - (slo.measurement_window_hours * 3600)
        
        metrics = self.calculate_reliability_metrics(agent_type, window_start)
        
        # Check success rate SLO
        if metrics.success_rate < slo.target_percentage:
            self._record_slo_violation(
                slo.slo_name,
                agent_type,
                "success_rate",
                metrics.success_rate,
                slo.target_percentage
            )
    
    def calculate_reliability_metrics(self, 
                                    agent_type: str, 
                                    since_timestamp: float) -> AgentReliabilityMetrics:
        """Calculate reliability metrics for an agent"""
        
        conn = sqlite3.connect(self.reliability_db)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT success, latency_ms, error_type 
        FROM agent_operations
        WHERE agent_type = ? AND start_time >= ?
        """, (agent_type, since_timestamp))
        
        operations = cursor.fetchall()
        conn.close()
        
        if not operations:
            return AgentReliabilityMetrics(
                agent_type=agent_type,
                success_rate=100.0,
                average_latency_ms=0.0,
                error_rate=0.0,
                availability=100.0,
                mean_time_to_recovery=0.0
            )
        
        total_operations = len(operations)
        successful_operations = sum(1 for op in operations if op[0])
        latencies = [op[1] for op in operations if op[1] is not None]
        
        success_rate = (successful_operations / total_operations) * 100
        error_rate = 100 - success_rate
        avg_latency = statistics.mean(latencies) if latencies else 0.0
        
        return AgentReliabilityMetrics(
            agent_type=agent_type,
            success_rate=success_rate,
            average_latency_ms=avg_latency,
            error_rate=error_rate,
            availability=success_rate,  # Simplified calculation
            mean_time_to_recovery=0.0  # Would require more complex calculation
        )
    
    def get_fallback_strategy(self, failed_agent: str, operation_type: str) -> str:
        """Get fallback agent when primary agent fails"""
        
        fallback_strategies = {
            "claude-build": "copilot-review",  # Fallback to review agent for building
            "copilot-review": "lightweight-cheap",  # Fallback to cheap agent for review
            "security-specialized": "claude-build",  # Fallback to general build agent
            "chatgpt-design": "claude-build"  # Fallback to Claude for design
        }
        
        return fallback_strategies.get(failed_agent, "lightweight-cheap")
    
    def _record_slo_violation(self, 
                             slo_name: str,
                             agent_type: str, 
                             violation_type: str,
                             actual_value: float,
                             target_value: float):
        """Record SLO violation for alerting"""
        
        conn = sqlite3.connect(self.reliability_db)
        cursor = conn.cursor()
        
        violation_id = f"{slo_name}_{violation_type}_{int(time.time())}"
        
        cursor.execute("""
        INSERT INTO slo_violations
        (violation_id, slo_name, agent_type, violation_type, actual_value, target_value, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (violation_id, slo_name, agent_type, violation_type, actual_value, target_value, time.time()))
        
        conn.commit()
        conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# 10. HUMAN COLLABORATION INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CognitiveSummary:
    """Optimized summary for human cognitive load"""
    risk_hotspots: List[str]
    architectural_impact: str
    confidence_score: float
    recommended_merge_action: str
    unusual_patterns: List[str]
    attention_required_areas: List[str]

class HumanCollaborationEngine:
    """Optimizes human cognitive load - supervisors, not validators"""
    
    def __init__(self):
        self.human_feedback_db = "human_collaboration.db"
        self._init_human_feedback_database()
    
    def _init_human_feedback_database(self):
        """Initialize human feedback tracking"""
        conn = sqlite3.connect(self.human_feedback_db)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS human_overrides (
            override_id TEXT PRIMARY KEY,
            original_decision TEXT,
            human_decision TEXT,
            reasoning TEXT,
            timestamp REAL,
            outcome_success BOOLEAN
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cognitive_load_metrics (
            session_id TEXT,
            review_time_seconds REAL,
            decisions_made INTEGER,
            overrides_used INTEGER,
            reported_difficulty INTEGER,  -- 1-10 scale
            timestamp REAL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def generate_cognitive_summary(self, 
                                 governance_decision: Dict[str, Any]) -> CognitiveSummary:
        """Generate human-optimized summary focusing on what requires attention"""
        
        risk_assessment = governance_decision.get("risk_assessment", {})
        system_impact = governance_decision.get("system_impact", {})
        arch_violations = governance_decision.get("architectural_violations", [])
        
        # Identify risk hotspots
        risk_hotspots = []
        if risk_assessment.get("overall_risk_score", 0) >= 7:
            risk_hotspots.extend(risk_assessment.get("recommended_actions", []))
        
        # Summarize architectural impact
        blast_radius = system_impact.get("blast_radius_score", 0)
        if blast_radius >= 7:
            arch_impact = f"HIGH IMPACT: Affects {len(system_impact.get('affected_services', []))} services"
        elif blast_radius >= 4:
            arch_impact = f"MEDIUM IMPACT: Limited service dependencies"
        else:
            arch_impact = "LOW IMPACT: Isolated changes"
        
        # Identify unusual patterns
        unusual_patterns = []
        if len(arch_violations) > 0:
            unusual_patterns.append(f"{len(arch_violations)} architectural violations detected")
        
        if system_impact.get("compliance_boundaries_crossed"):
            unusual_patterns.append("Crosses compliance boundaries")
        
        # Determine recommended action
        confidence = governance_decision.get("confidence_score", 0.5)
        risk_score = risk_assessment.get("overall_risk_score", 0)

        if confidence >= 0.9 and risk_score < 5:
            recommendation = "APPROVE"
        elif risk_score >= 8:
            recommendation = "HOLD - Security Review Required"
        elif len(arch_violations) > 2:
            recommendation = "HOLD"
        else:
            recommendation = "REVIEW"
        
        # Areas requiring attention
        attention_areas = []
        if risk_score >= 7:
            attention_areas.append("Security implications")
        if len(arch_violations) > 0:
            attention_areas.append("Architectural compliance")
        if blast_radius >= 6:
            attention_areas.append("System-wide impact")
        
        return CognitiveSummary(
            risk_hotspots=risk_hotspots[:3],  # Limit to top 3
            architectural_impact=arch_impact,
            confidence_score=confidence,
            recommended_merge_action=recommendation,
            unusual_patterns=unusual_patterns,
            attention_required_areas=attention_areas
        )
    
    def record_human_override(self, 
                            original_decision: str,
                            human_decision: str, 
                            reasoning: str) -> str:
        """Record human override for system learning"""
        
        conn = sqlite3.connect(self.human_feedback_db)
        cursor = conn.cursor()
        
        override_id = f"override_{int(time.time())}"
        
        cursor.execute("""
        INSERT INTO human_overrides
        (override_id, original_decision, human_decision, reasoning, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (override_id, original_decision, human_decision, reasoning, time.time()))
        
        conn.commit()
        conn.close()
        
        return override_id
    
    def analyze_human_ai_collaboration_patterns(self) -> Dict[str, Any]:
        """Analyze human-AI collaboration effectiveness"""
        
        conn = sqlite3.connect(self.human_feedback_db)
        cursor = conn.cursor()
        
        # Get override patterns
        cursor.execute("""
        SELECT original_decision, human_decision, COUNT(*)
        FROM human_overrides
        GROUP BY original_decision, human_decision
        """)
        
        override_patterns = cursor.fetchall()
        
        # Get cognitive load metrics
        cursor.execute("""
        SELECT AVG(review_time_seconds), AVG(reported_difficulty), AVG(overrides_used)
        FROM cognitive_load_metrics
        WHERE timestamp >= ?
        """, (time.time() - (30 * 24 * 3600),))  # Last 30 days
        
        cognitive_metrics = cursor.fetchone()
        conn.close()
        
        return {
            "override_patterns": [
                {"original": orig, "human": human, "frequency": count}
                for orig, human, count in override_patterns
            ],
            "average_review_time_seconds": cognitive_metrics[0] if cognitive_metrics[0] else 0,
            "average_difficulty_reported": cognitive_metrics[1] if cognitive_metrics[1] else 0,
            "average_overrides_per_session": cognitive_metrics[2] if cognitive_metrics[2] else 0
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 11. COMPLIANCE & AUDIT INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ComplianceEvidence:
    """Automatically generated compliance evidence"""
    requirement_id: str
    evidence_type: str
    evidence_data: Dict[str, Any]
    verification_method: str
    timestamp: float
    compliance_officer: str

@dataclass 
class AuditTrail:
    """Complete audit trail for compliance"""
    change_id: str
    requirement_source: str
    design_decision: Dict[str, Any]
    code_implementation: Dict[str, Any]
    review_evidence: Dict[str, Any]
    remediation_actions: List[Dict[str, Any]]
    approval_chain: List[Dict[str, Any]]
    deployment_evidence: Dict[str, Any]

class ComplianceAuditEngine:
    """AI-native compliance engineering for regulated industries"""
    
    def __init__(self):
        self.compliance_db = "compliance_audit.db"
        self._init_compliance_database()
        self.compliance_frameworks = self._load_compliance_frameworks()
    
    def _init_compliance_database(self):
        """Initialize compliance and audit database"""
        conn = sqlite3.connect(self.compliance_db)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_trails (
            change_id TEXT PRIMARY KEY,
            requirement_source TEXT,
            evidence_json TEXT,
            compliance_status TEXT,
            audit_timestamp REAL,
            compliance_officer TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS compliance_violations (
            violation_id TEXT PRIMARY KEY,
            framework TEXT,
            requirement_id TEXT,
            violation_description TEXT,
            severity TEXT,
            remediation_required TEXT,
            timestamp REAL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS policy_lineage (
            lineage_id TEXT PRIMARY KEY,
            requirement_id TEXT,
            design_reference TEXT,
            code_reference TEXT,
            test_reference TEXT,
            deployment_reference TEXT,
            traceability_score REAL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def _load_compliance_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """Load compliance framework requirements"""
        return {
            "SOX": {
                "change_approval": "required_dual_approval",
                "audit_trail": "complete_change_lineage",
                "segregation_of_duties": "developer_cannot_approve_own_changes"
            },
            "GDPR": {
                "data_protection": "pii_handling_verification",
                "consent_management": "explicit_consent_tracking",
                "right_to_deletion": "data_deletion_capability"
            },
            "PCI_DSS": {
                "card_data_protection": "encryption_at_rest_and_transit", 
                "access_control": "least_privilege_principle",
                "security_testing": "mandatory_security_scan"
            },
            "HIPAA": {
                "phi_protection": "healthcare_data_encryption",
                "access_logging": "complete_access_audit_trail",
                "breach_notification": "automated_breach_detection"
            },
            "ISO_27001": {
                "information_security": "security_by_design",
                "risk_management": "continuous_risk_assessment",
                "incident_response": "automated_incident_tracking"
            }
        }
    
    def generate_compliance_evidence(self, 
                                   change_request: Dict[str, Any],
                                   governance_decision: Dict[str, Any]) -> List[ComplianceEvidence]:
        """Generate automatic compliance evidence"""
        
        evidence_list = []
        
        # Determine applicable frameworks
        applicable_frameworks = self._identify_applicable_frameworks(change_request)
        
        for framework in applicable_frameworks:
            framework_requirements = self.compliance_frameworks.get(framework, {})
            
            for requirement_id, requirement_desc in framework_requirements.items():
                evidence = self._generate_evidence_for_requirement(
                    framework, 
                    requirement_id,
                    requirement_desc,
                    change_request,
                    governance_decision
                )
                
                if evidence:
                    evidence_list.append(evidence)
        
        return evidence_list
    
    def _identify_applicable_frameworks(self, change_request: Dict[str, Any]) -> List[str]:
        """Identify which compliance frameworks apply to this change"""
        
        applicable = []
        
        component = change_request.get("component", "").lower()
        description = change_request.get("description", "").lower()
        
        # Banking/Financial Services
        if any(term in component or term in description for term in ['payment', 'billing', 'financial']):
            applicable.extend(["SOX", "PCI_DSS"])
        
        # Healthcare
        if any(term in component or term in description for term in ['health', 'medical', 'patient']):
            applicable.extend(["HIPAA"])
        
        # Data handling
        if any(term in component or term in description for term in ['user', 'customer', 'personal', 'pii']):
            applicable.extend(["GDPR"])
        
        # Security-related changes
        if any(term in component or term in description for term in ['security', 'auth', 'encryption']):
            applicable.extend(["ISO_27001"])
        
        # Default: Apply SOX for all financial institutions
        if change_request.get("regulated", False):
            applicable.append("SOX")
        
        return list(set(applicable))  # Remove duplicates
    
    def _generate_evidence_for_requirement(self, 
                                         framework: str,
                                         requirement_id: str, 
                                         requirement_desc: str,
                                         change_request: Dict[str, Any],
                                         governance_decision: Dict[str, Any]) -> Optional[ComplianceEvidence]:
        """Generate specific evidence for a compliance requirement"""
        
        evidence_data = {}
        
        if requirement_id == "change_approval":
            evidence_data = {
                "approval_chain": governance_decision.get("governance_requirements", {}),
                "dual_approval_required": governance_decision.get("risk_assessment", {}).get("overall_risk_score", 0) >= 7,
                "approvers": ["ai_governance_system", "human_reviewer_required"]
            }
        
        elif requirement_id == "audit_trail":
            evidence_data = {
                "complete_lineage": True,
                "design_reference": f"design_issue_linked",
                "code_implementation": f"pr_linked_to_design", 
                "review_evidence": governance_decision.get("agent_explanation", {}),
                "deployment_governance": governance_decision.get("governance_requirements", {})
            }
        
        elif requirement_id == "security_testing":
            evidence_data = {
                "security_scan_required": governance_decision.get("risk_assessment", {}).get("overall_risk_score", 0) >= 8,
                "automated_security_checks": True,
                "security_agent_review": governance_decision.get("selected_agent") == "security-specialized"
            }
        
        elif requirement_id == "segregation_of_duties":
            evidence_data = {
                "developer_cannot_self_approve": True,
                "ai_agent_separation": {
                    "design_agent": "chatgpt",
                    "build_agent": "claude",
                    "review_agent": "copilot"
                },
                "human_approval_required": True
            }

        elif requirement_id == "information_security":
            evidence_data = {
                "security_by_design": True,
                "risk_assessment_performed": True,
                "security_agent_available": governance_decision.get("selected_agent") == "security-specialized",
                "security_controls": governance_decision.get("governance_requirements", {})
            }

        elif requirement_id == "risk_management":
            evidence_data = {
                "risk_score": governance_decision.get("risk_assessment", {}).get("overall_risk_score", 0),
                "risk_factors": governance_decision.get("risk_assessment", {}).get("risk_factors", {}),
                "continuous_assessment": True
            }

        elif requirement_id == "incident_response":
            evidence_data = {
                "automated_detection": True,
                "governance_system_active": True,
                "fallback_mechanisms": "enabled"
            }

        if evidence_data:
            return ComplianceEvidence(
                requirement_id=f"{framework}_{requirement_id}",
                evidence_type="automated_governance_evidence",
                evidence_data=evidence_data,
                verification_method="ai_governance_system",
                timestamp=time.time(),
                compliance_officer="ai_compliance_engine"
            )
        
        return None
    
    def create_audit_trail(self, 
                          change_id: str,
                          requirement_source: str,
                          governance_decision: Dict[str, Any]) -> AuditTrail:
        """Create complete audit trail for compliance"""
        
        return AuditTrail(
            change_id=change_id,
            requirement_source=requirement_source,
            design_decision={
                "agent_used": "chatgpt-design",
                "design_approved": True,
                "design_timestamp": time.time()
            },
            code_implementation={
                "agent_used": governance_decision.get("selected_agent"),
                "implementation_governance": governance_decision.get("governance_requirements"),
                "risk_assessment": governance_decision.get("risk_assessment")
            },
            review_evidence={
                "automated_review": True,
                "ai_review_agent": "copilot-review", 
                "review_outcome": "pending_human_approval"
            },
            remediation_actions=governance_decision.get("recommended_actions", []),
            approval_chain=[
                {"level": "ai_governance", "status": "approved", "timestamp": time.time()},
                {"level": "human_review", "status": "pending", "timestamp": None}
            ],
            deployment_evidence={
                "governance_evidence": "complete",
                "deployment_controls": governance_decision.get("governance_requirements", {})
            }
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 12. BENCHMARKABLE METRICS SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class EngineeringMetrics:
    """Measurable engineering delivery metrics"""
    escaped_defects_reduction: float
    pr_review_time_reduction: float
    remediation_automation_percentage: float
    cost_savings_dollars: float
    policy_violation_reduction: float
    developer_productivity_improvement: float
    rollback_reduction_percentage: float
    security_issue_prevention_count: int

class BenchmarkableMetricsEngine:
    """Makes uniqueness measurable - transforms vision into enterprise-buyable metrics"""
    
    def __init__(self):
        self.metrics_db = "benchmarkable_metrics.db"
        self._init_metrics_database()
    
    def _init_metrics_database(self):
        """Initialize metrics tracking database"""
        conn = sqlite3.connect(self.metrics_db)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS engineering_metrics (
            metric_id TEXT PRIMARY KEY,
            metric_type TEXT,
            metric_value REAL,
            baseline_value REAL,
            improvement_percentage REAL,
            measurement_period_days INTEGER,
            timestamp REAL,
            repository TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productivity_metrics (
            session_id TEXT PRIMARY KEY,
            developer_id TEXT,
            changes_delivered INTEGER,
            review_cycles_reduced INTEGER,
            automation_time_saved_minutes REAL,
            manual_work_eliminated_minutes REAL,
            timestamp REAL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_metrics (
            quality_event_id TEXT PRIMARY KEY,
            event_type TEXT,  -- 'defect_prevented', 'rollback_avoided', 'security_issue_blocked'
            severity TEXT,
            prevention_method TEXT,
            cost_impact_avoided REAL,
            timestamp REAL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def calculate_engineering_metrics(self, 
                                    baseline_period_days: int = 90,
                                    measurement_period_days: int = 30) -> EngineeringMetrics:
        """Calculate comprehensive engineering delivery metrics"""
        
        baseline_start = time.time() - ((baseline_period_days + measurement_period_days) * 24 * 3600)
        baseline_end = time.time() - (measurement_period_days * 24 * 3600)
        measurement_start = baseline_end
        measurement_end = time.time()
        
        # Calculate baseline metrics
        baseline_metrics = self._calculate_period_metrics(baseline_start, baseline_end)
        
        # Calculate current period metrics
        current_metrics = self._calculate_period_metrics(measurement_start, measurement_end)
        
        # Calculate improvements
        metrics = EngineeringMetrics(
            escaped_defects_reduction=self._calculate_percentage_improvement(
                baseline_metrics.get("escaped_defects", 0),
                current_metrics.get("escaped_defects", 0)
            ),
            pr_review_time_reduction=self._calculate_percentage_improvement(
                baseline_metrics.get("avg_review_time", 0),
                current_metrics.get("avg_review_time", 0)
            ),
            remediation_automation_percentage=current_metrics.get("automation_percentage", 0),
            cost_savings_dollars=baseline_metrics.get("total_cost", 0) - current_metrics.get("total_cost", 0),
            policy_violation_reduction=self._calculate_percentage_improvement(
                baseline_metrics.get("policy_violations", 0),
                current_metrics.get("policy_violations", 0)
            ),
            developer_productivity_improvement=self._calculate_percentage_improvement(
                baseline_metrics.get("changes_per_developer", 0),
                current_metrics.get("changes_per_developer", 0)
            ),
            rollback_reduction_percentage=self._calculate_percentage_improvement(
                baseline_metrics.get("rollback_count", 0),
                current_metrics.get("rollback_count", 0)
            ),
            security_issue_prevention_count=current_metrics.get("security_issues_prevented", 0)
        )
        
        # Store metrics
        self._store_metrics(metrics, measurement_period_days)
        
        return metrics
    
    def _calculate_period_metrics(self, start_time: float, end_time: float) -> Dict[str, float]:
        """Calculate metrics for a specific time period"""
        
        conn = sqlite3.connect(self.metrics_db)
        cursor = conn.cursor()
        
        # Get quality metrics for the period
        cursor.execute("""
        SELECT event_type, COUNT(*), AVG(cost_impact_avoided)
        FROM quality_metrics
        WHERE timestamp BETWEEN ? AND ?
        GROUP BY event_type
        """, (start_time, end_time))
        
        quality_results = cursor.fetchall()
        
        # Get productivity metrics for the period
        cursor.execute("""
        SELECT 
            COUNT(*) as sessions,
            AVG(changes_delivered) as avg_changes,
            AVG(automation_time_saved_minutes) as avg_automation_time,
            SUM(manual_work_eliminated_minutes) as total_manual_saved
        FROM productivity_metrics
        WHERE timestamp BETWEEN ? AND ?
        """, (start_time, end_time))
        
        productivity_result = cursor.fetchone()
        
        conn.close()
        
        # Process results
        period_metrics = {
            "escaped_defects": 0,
            "rollback_count": 0,
            "security_issues_prevented": 0,
            "avg_review_time": 120,  # Default 2 hours
            "automation_percentage": 0,
            "policy_violations": 0,
            "changes_per_developer": 0,
            "total_cost": 0
        }
        
        for event_type, count, avg_cost in quality_results:
            if event_type == "defect_prevented":
                period_metrics["escaped_defects"] = max(0, 10 - count)  # Assume baseline of 10 defects
            elif event_type == "rollback_avoided":
                period_metrics["rollback_count"] = max(0, 5 - count)  # Assume baseline of 5 rollbacks
            elif event_type == "security_issue_blocked":
                period_metrics["security_issues_prevented"] = count
        
        if productivity_result and productivity_result[0]:
            period_metrics["changes_per_developer"] = productivity_result[1] or 0
            period_metrics["automation_percentage"] = min(100, (productivity_result[2] or 0) / 60 * 100)  # Convert to percentage
        
        return period_metrics
    
    def _calculate_percentage_improvement(self, baseline: float, current: float) -> float:
        """Calculate percentage improvement (positive means better)"""
        
        if baseline == 0:
            return 0.0
        
        # For metrics where lower is better (defects, review time, violations, rollbacks)
        return ((baseline - current) / baseline) * 100
    
    def record_quality_event(self,
                           event_type: str,
                           severity: str,
                           prevention_method: str,
                           cost_impact_avoided: float = 0):
        """Record quality improvement event"""

        event_id = f"{event_type}_{time.time_ns()}"
        conn = sqlite3.connect(self.metrics_db)
        try:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR IGNORE INTO quality_metrics
            (quality_event_id, event_type, severity, prevention_method, cost_impact_avoided, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (event_id, event_type, severity, prevention_method, cost_impact_avoided, time.time()))
            conn.commit()
        finally:
            conn.close()
    
    def _store_metrics(self, metrics: EngineeringMetrics, period_days: int):
        """Store calculated metrics for reporting"""

        metrics_to_store = [
            ("escaped_defects_reduction", metrics.escaped_defects_reduction),
            ("pr_review_time_reduction", metrics.pr_review_time_reduction),
            ("remediation_automation_percentage", metrics.remediation_automation_percentage),
            ("cost_savings_dollars", metrics.cost_savings_dollars),
            ("policy_violation_reduction", metrics.policy_violation_reduction),
            ("developer_productivity_improvement", metrics.developer_productivity_improvement),
            ("rollback_reduction_percentage", metrics.rollback_reduction_percentage),
            ("security_issue_prevention_count", float(metrics.security_issue_prevention_count))
        ]

        conn = sqlite3.connect(self.metrics_db)
        try:
            cursor = conn.cursor()
            for metric_type, value in metrics_to_store:
                metric_id = f"{metric_type}_{time.time_ns()}"
                cursor.execute("""
                INSERT OR IGNORE INTO engineering_metrics
                (metric_id, metric_type, metric_value, measurement_period_days, timestamp, repository)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (metric_id, metric_type, value, period_days, time.time(), "all_repositories"))
            conn.commit()
        finally:
            conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# 13. DEVELOPER TRUST & ADOPTION STRATEGY
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AdoptionMetrics:
    """Developer adoption and trust metrics"""
    override_frequency: float
    developer_satisfaction_score: float
    system_bypass_attempts: int
    positive_feedback_percentage: float
    time_to_trust: float  # Days until developers stop overriding frequently

class DeveloperTrustEngine:
    """Prevents AI bureaucracy through adaptive strictness and trust-building"""
    
    def __init__(self):
        self.trust_db = "developer_trust.db"
        self._init_trust_database()
        self.strictness_levels = self._initialize_strictness_levels()
    
    def _init_trust_database(self):
        """Initialize developer trust tracking"""
        conn = sqlite3.connect(self.trust_db)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS developer_feedback (
            feedback_id TEXT PRIMARY KEY,
            developer_id TEXT,
            decision_id TEXT,
            feedback_type TEXT,  -- 'positive', 'negative', 'override'
            feedback_text TEXT,
            satisfaction_score INTEGER,  -- 1-10
            timestamp REAL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS adaptation_history (
            adaptation_id TEXT PRIMARY KEY,
            trigger_event TEXT,
            old_strictness_level TEXT,
            new_strictness_level TEXT,
            adaptation_reason TEXT,
            timestamp REAL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trust_metrics (
            metric_id TEXT PRIMARY KEY,
            developer_id TEXT,
            trust_score REAL,  -- 0.0-1.0
            override_frequency REAL,
            positive_interactions INTEGER,
            negative_interactions INTEGER,
            measurement_date REAL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def _initialize_strictness_levels(self) -> Dict[str, Dict[str, Any]]:
        """Initialize adaptive strictness levels"""
        return {
            "learning": {
                "ai_intervention_threshold": 8,  # Only intervene on high-risk changes
                "explanations": "detailed",
                "override_friction": "minimal",
                "educational_prompts": True
            },
            "standard": {
                "ai_intervention_threshold": 6,
                "explanations": "standard", 
                "override_friction": "normal",
                "educational_prompts": False
            },
            "strict": {
                "ai_intervention_threshold": 4,
                "explanations": "brief",
                "override_friction": "moderate",
                "educational_prompts": False
            },
            "maximum": {
                "ai_intervention_threshold": 2,
                "explanations": "minimal",
                "override_friction": "high",
                "educational_prompts": False
            }
        }
    
    def adapt_strictness_for_developer(self, 
                                     developer_id: str,
                                     recent_interactions: List[Dict[str, Any]]) -> str:
        """Adapt system strictness based on developer behavior and trust"""
        
        # Calculate current trust metrics
        trust_metrics = self._calculate_developer_trust(developer_id, recent_interactions)
        
        current_strictness = self._get_current_strictness(developer_id)
        new_strictness = current_strictness
        
        # Adapt based on trust and behavior patterns
        if trust_metrics["override_frequency"] > 0.5 and trust_metrics["satisfaction_score"] < 4:
            # High overrides + low satisfaction = too strict
            new_strictness = self._decrease_strictness(current_strictness)
            adaptation_reason = "High override frequency with low satisfaction"
            
        elif trust_metrics["override_frequency"] < 0.1 and trust_metrics["satisfaction_score"] > 7:
            # Low overrides + high satisfaction = potentially increase strictness for efficiency
            new_strictness = self._increase_strictness(current_strictness)
            adaptation_reason = "Low override frequency with high satisfaction"
            
        elif trust_metrics["bypass_attempts"] > 2:
            # System bypass attempts = too controlling
            new_strictness = "learning"
            adaptation_reason = "Developer attempting to bypass system"
        
        else:
            adaptation_reason = "No adaptation needed"
        
        # Record adaptation if changed
        if new_strictness != current_strictness:
            self._record_adaptation(developer_id, current_strictness, new_strictness, adaptation_reason)
        
        return new_strictness
    
    def _calculate_developer_trust(self, 
                                 developer_id: str, 
                                 recent_interactions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate developer trust metrics"""
        
        if not recent_interactions:
            return {
                "override_frequency": 0.0,
                "satisfaction_score": 5.0,
                "bypass_attempts": 0,
                "positive_feedback_percentage": 50.0
            }
        
        total_interactions = len(recent_interactions)
        overrides = sum(1 for interaction in recent_interactions if interaction.get("type") == "override")
        bypasses = sum(1 for interaction in recent_interactions if interaction.get("type") == "bypass")
        
        satisfaction_scores = [
            interaction.get("satisfaction", 5) 
            for interaction in recent_interactions 
            if interaction.get("satisfaction")
        ]
        avg_satisfaction = statistics.mean(satisfaction_scores) if satisfaction_scores else 5.0
        
        positive_feedback = sum(1 for interaction in recent_interactions 
                              if interaction.get("feedback_type") == "positive")
        
        return {
            "override_frequency": overrides / total_interactions,
            "satisfaction_score": avg_satisfaction,
            "bypass_attempts": bypasses,
            "positive_feedback_percentage": (positive_feedback / total_interactions) * 100
        }
    
    def _get_current_strictness(self, developer_id: str) -> str:
        """Get current strictness level for developer"""
        default_strictness = "standard"
        
        try:
            conn = sqlite3.connect(self.trust_db)
            cursor = conn.cursor()
            cursor.execute("""
            SELECT new_strictness
            FROM adaptation_history
            WHERE developer_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """, (developer_id,))
            
            row = cursor.fetchone()
            conn.close()
        except sqlite3.Error:
            return default_strictness
        
        if not row or not row[0]:
            return default_strictness
        
        current_strictness = row[0]
        if current_strictness in self.strictness_levels:
            return current_strictness
        
        return default_strictness
    
    def _decrease_strictness(self, current: str) -> str:
        """Decrease strictness level"""
        strictness_order = ["maximum", "strict", "standard", "learning"]
        current_index = strictness_order.index(current) if current in strictness_order else 2
        return strictness_order[min(len(strictness_order) - 1, current_index + 1)]
    
    def _increase_strictness(self, current: str) -> str:
        """Increase strictness level"""
        strictness_order = ["learning", "standard", "strict", "maximum"]
        current_index = strictness_order.index(current) if current in strictness_order else 1
        return strictness_order[min(len(strictness_order) - 1, current_index + 1)]
    
    def record_developer_feedback(self, 
                                developer_id: str,
                                decision_id: str,
                                feedback_type: str,
                                satisfaction_score: int,
                                feedback_text: str = ""):
        """Record developer feedback for trust building"""
        
        conn = sqlite3.connect(self.trust_db)
        cursor = conn.cursor()
        
        feedback_id = f"feedback_{developer_id}_{int(time.time())}"
        
        cursor.execute("""
        INSERT INTO developer_feedback
        (feedback_id, developer_id, decision_id, feedback_type, feedback_text, satisfaction_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (feedback_id, developer_id, decision_id, feedback_type, feedback_text, satisfaction_score, time.time()))
        
        conn.commit()
        conn.close()
    
    def _record_adaptation(self, 
                          developer_id: str,
                          old_strictness: str, 
                          new_strictness: str,
                          reason: str):
        """Record strictness adaptation"""
        
        conn = sqlite3.connect(self.trust_db)
        cursor = conn.cursor()
        
        adaptation_id = f"adapt_{developer_id}_{int(time.time())}"
        
        cursor.execute("""
        INSERT INTO adaptation_history
        (adaptation_id, trigger_event, old_strictness_level, new_strictness_level, adaptation_reason, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (adaptation_id, f"developer_{developer_id}_behavior", old_strictness, new_strictness, reason, time.time()))
        
        conn.commit()
        conn.close()
    
    def generate_trust_report(self) -> Dict[str, Any]:
        """Generate developer trust and adoption report"""
        
        conn = sqlite3.connect(self.trust_db)
        cursor = conn.cursor()
        
        # Get overall satisfaction metrics
        cursor.execute("""
        SELECT 
            AVG(satisfaction_score) as avg_satisfaction,
            COUNT(*) as total_feedback,
            SUM(CASE WHEN feedback_type = 'positive' THEN 1 ELSE 0 END) as positive_count,
            SUM(CASE WHEN feedback_type = 'override' THEN 1 ELSE 0 END) as override_count
        FROM developer_feedback
        WHERE timestamp >= ?
        """, (time.time() - (30 * 24 * 3600),))  # Last 30 days
        
        satisfaction_metrics = cursor.fetchone()
        
        # Get adaptation frequency
        cursor.execute("""
        SELECT COUNT(*) as adaptations
        FROM adaptation_history
        WHERE timestamp >= ?
        """, (time.time() - (30 * 24 * 3600),))
        
        adaptations = cursor.fetchone()[0]
        
        conn.close()
        
        if satisfaction_metrics and satisfaction_metrics[1] > 0:  # Has feedback
            return {
                "average_satisfaction_score": satisfaction_metrics[0] or 5.0,
                "total_feedback_received": satisfaction_metrics[1],
                "positive_feedback_percentage": (satisfaction_metrics[2] / satisfaction_metrics[1]) * 100 if satisfaction_metrics[1] > 0 else 0,
                "override_frequency": (satisfaction_metrics[3] / satisfaction_metrics[1]) * 100 if satisfaction_metrics[1] > 0 else 0,
                "system_adaptations_last_30_days": adaptations,
                "trust_building_status": "active" if adaptations > 0 else "stable"
            }
        else:
            return {
                "average_satisfaction_score": 5.0,
                "total_feedback_received": 0,
                "positive_feedback_percentage": 0,
                "override_frequency": 0,
                "system_adaptations_last_30_days": 0,
                "trust_building_status": "insufficient_data"
            }