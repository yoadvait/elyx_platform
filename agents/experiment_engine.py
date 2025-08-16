# Experiment Engine - Transform suggestions into structured experiments
# Based on Hackathon Implementation Guide Phase 2

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ExperimentStatus(Enum):
    PLANNED = "planned"
    RUNNING = "running" 
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class ExperimentTemplate:
    name: str
    hypothesis_template: str
    protocol: Dict
    success_criteria: Dict
    duration_days: int
    measurements: List[str]


# Experiment templates from Implementation Guide
EXPERIMENT_TEMPLATES = {
    "SLEEP_OPTIMIZATION": ExperimentTemplate(
        name="Sleep Optimization",
        hypothesis_template="Blue light blocking glasses after 4pm will improve deep sleep quality",
        protocol={
            "intervention": "Wear blue-light glasses during evening screen time",
            "duration": "2 weeks",
            "measurements": ["sleep_latency", "deep_sleep_minutes", "sleep_disturbances"],
            "adherence_tracking": "daily_checklist"
        },
        success_criteria={
            "primary": "deep_sleep_increase > 20%",
            "secondary": "sleep_latency_decrease > 30%"
        },
        duration_days=14,
        measurements=["sleep_latency", "deep_sleep_minutes", "sleep_disturbances"]
    ),
    
    "NUTRITION_INTERVENTION": ExperimentTemplate(
        name="Nutrition Intervention",
        hypothesis_template="Soaking legumes overnight will reduce digestive issues",
        protocol={
            "intervention": "Chef soaks all legumes 12+ hours before cooking",
            "duration": "1 week", 
            "measurements": ["bloating_score", "digestive_comfort"],
            "adherence_tracking": "chef_confirmation"
        },
        success_criteria={
            "primary": "bloating_score_decrease > 30%",
            "secondary": "digestive_comfort_increase > 25%"
        },
        duration_days=7,
        measurements=["bloating_score", "digestive_comfort"]
    ),
    
    "SUPPLEMENT_TRIAL": ExperimentTemplate(
        name="Supplement Trial",
        hypothesis_template="Magnesium threonate 400mg before bed will improve sleep quality",
        protocol={
            "intervention": "Take magnesium threonate 400mg 1 hour before bedtime",
            "duration": "3 weeks",
            "measurements": ["sleep_latency", "sleep_quality_score", "morning_alertness"],
            "adherence_tracking": "daily_log"
        },
        success_criteria={
            "primary": "sleep_latency_decrease > 25%",
            "secondary": "sleep_quality_score_increase > 20%"
        },
        duration_days=21,
        measurements=["sleep_latency", "sleep_quality_score", "morning_alertness"]
    ),
    
    "EXERCISE_PROTOCOL": ExperimentTemplate(
        name="Exercise Protocol",
        hypothesis_template="Morning HIIT sessions will improve HRV without affecting recovery",
        protocol={
            "intervention": "15-minute HIIT session 3x/week at 7am",
            "duration": "4 weeks",
            "measurements": ["hrv", "recovery_score", "workout_performance"],
            "adherence_tracking": "whoop_data"
        },
        success_criteria={
            "primary": "hrv_increase > 15%",
            "secondary": "recovery_score_maintained > 80%"
        },
        duration_days=28,
        measurements=["hrv", "recovery_score", "workout_performance"]
    ),
    
    "CGM_MEAL_TEST": ExperimentTemplate(
        name="CGM Meal Test",
        hypothesis_template="Eating protein before carbs will reduce glucose spike by 30%",
        protocol={
            "intervention": "Consume protein portion 10 minutes before carbohydrates",
            "duration": "10 days",
            "measurements": ["glucose_peak", "glucose_auc", "time_to_baseline"],
            "adherence_tracking": "meal_photo_timestamps"
        },
        success_criteria={
            "primary": "glucose_peak_reduction > 30%",
            "secondary": "time_to_baseline_decrease > 20%"
        },
        duration_days=10,
        measurements=["glucose_peak", "glucose_auc", "time_to_baseline"]
    )
}


@dataclass
class ExperimentMeasurement:
    name: str
    value: float
    timestamp: datetime
    raw_data: Optional[Dict] = None


@dataclass 
class Experiment:
    id: str
    template_name: Optional[str]
    hypothesis: str
    protocol: Dict
    member_id: str
    status: ExperimentStatus
    created_at: datetime
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    measurements: List[ExperimentMeasurement] = None
    outcome: Optional[str] = None
    success: Optional[bool] = None
    
    def __post_init__(self):
        if self.measurements is None:
            self.measurements = []


class ExperimentEngine:
    """Transform member issues into structured experiments with measurable outcomes"""
    
    def __init__(self):
        self.active_experiments: Dict[str, Experiment] = {}
        self.completed_experiments: List[Experiment] = []
    
    def propose_experiment(self, member_issue: str, agent_context: Optional[Dict] = None) -> Dict:
        """Propose an experiment based on member issue"""
        template = self._select_template(member_issue)
        if not template:
            return self._create_custom_experiment(member_issue, agent_context)
        
        customized_experiment = self._customize_for_member(template, member_issue, agent_context)
        
        return {
            "experiment": customized_experiment,
            "rationale": self._generate_rationale(customized_experiment, member_issue),
            "expected_outcome": self._predict_outcome(customized_experiment)
        }
    
    def _select_template(self, member_issue: str) -> Optional[ExperimentTemplate]:
        """Select appropriate experiment template based on issue"""
        issue_lower = member_issue.lower()
        
        # Sleep-related issues
        if any(word in issue_lower for word in ["sleep", "insomnia", "tired", "fatigue", "rest"]):
            if "supplement" in issue_lower or "magnesium" in issue_lower:
                return EXPERIMENT_TEMPLATES["SUPPLEMENT_TRIAL"]
            return EXPERIMENT_TEMPLATES["SLEEP_OPTIMIZATION"]
        
        # Nutrition/digestive issues
        if any(word in issue_lower for word in ["bloating", "digestion", "stomach", "food", "meal"]):
            if "glucose" in issue_lower or "cgm" in issue_lower or "blood sugar" in issue_lower:
                return EXPERIMENT_TEMPLATES["CGM_MEAL_TEST"]
            return EXPERIMENT_TEMPLATES["NUTRITION_INTERVENTION"]
        
        # Exercise/performance issues
        if any(word in issue_lower for word in ["exercise", "workout", "performance", "hrv", "recovery"]):
            return EXPERIMENT_TEMPLATES["EXERCISE_PROTOCOL"]
        
        # Glucose/metabolic issues
        if any(word in issue_lower for word in ["glucose", "blood sugar", "metabolic", "cgm"]):
            return EXPERIMENT_TEMPLATES["CGM_MEAL_TEST"]
        
        return None
    
    def _customize_for_member(self, template: ExperimentTemplate, issue: str, context: Optional[Dict]) -> Dict:
        """Customize experiment template for specific member and issue"""
        member_id = context.get("member_id", "rohan") if context else "rohan"
        
        # Customize hypothesis based on specific issue
        hypothesis = self._customize_hypothesis(template.hypothesis_template, issue)
        
        # Adjust protocol for member constraints
        protocol = template.protocol.copy()
        if context and "travel_schedule" in context:
            protocol = self._adjust_for_travel(protocol)
        
        experiment_id = f"exp_{uuid.uuid4().hex[:8]}"
        
        return {
            "id": experiment_id,
            "template": template.name,
            "hypothesis": hypothesis,
            "protocol": protocol,
            "success_criteria": template.success_criteria,
            "duration_days": template.duration_days,
            "member_id": member_id,
            "measurements": template.measurements,
            "status": ExperimentStatus.PLANNED.value
        }
    
    def _customize_hypothesis(self, template: str, issue: str) -> str:
        """Customize hypothesis template based on specific issue"""
        # Simple customization - in production would use LLM
        if "sleep" in issue.lower() and "magnesium" not in template:
            return template.replace("Blue light blocking glasses", "Sleep hygiene protocol")
        return template
    
    def _adjust_for_travel(self, protocol: Dict) -> Dict:
        """Adjust protocol for travel constraints"""
        adjusted = protocol.copy()
        if "intervention" in adjusted:
            adjusted["travel_variant"] = "Simplified protocol for travel weeks"
        return adjusted
    
    def _create_custom_experiment(self, issue: str, context: Optional[Dict]) -> Dict:
        """Create custom experiment when no template matches"""
        experiment_id = f"exp_{uuid.uuid4().hex[:8]}"
        
        return {
            "experiment": {
                "id": experiment_id,
                "template": None,
                "hypothesis": f"Addressing '{issue}' will improve member satisfaction and outcomes",
                "protocol": {
                    "intervention": "Custom intervention based on member issue",
                    "duration": "2 weeks",
                    "measurements": ["satisfaction_score", "symptom_severity"],
                    "adherence_tracking": "daily_checklist"
                },
                "success_criteria": {"primary": "symptom_improvement > 50%"},
                "duration_days": 14,
                "member_id": context.get("member_id", "rohan") if context else "rohan",
                "measurements": ["satisfaction_score", "symptom_severity"],
                "status": ExperimentStatus.PLANNED.value
            },
            "rationale": f"Custom experiment designed to address specific member concern: {issue}",
            "expected_outcome": "Measurable improvement in reported symptoms"
        }
    
    def _generate_rationale(self, experiment: Dict, issue: str) -> str:
        """Generate rationale for the experiment"""
        return f"Based on member issue '{issue}', this experiment tests the hypothesis: {experiment['hypothesis']}. Expected to show measurable improvement within {experiment['duration_days']} days."
    
    def _predict_outcome(self, experiment: Dict) -> str:
        """Predict expected outcome"""
        criteria = experiment.get("success_criteria", {})
        primary = criteria.get("primary", "improvement")
        return f"Expected outcome: {primary} with high confidence based on similar interventions"
    
    def start_experiment(self, experiment_id: str) -> bool:
        """Start a planned experiment"""
        if experiment_id in self.active_experiments:
            experiment = self.active_experiments[experiment_id]
            if experiment.status == ExperimentStatus.PLANNED:
                experiment.status = ExperimentStatus.RUNNING
                experiment.start_date = datetime.now()
                experiment.end_date = datetime.now() + timedelta(days=experiment.protocol.get("duration_days", 14))
                return True
        return False
    
    def add_measurement(self, experiment_id: str, measurement_name: str, value: float, timestamp: Optional[datetime] = None, raw_data: Optional[Dict] = None) -> bool:
        """Add measurement to running experiment"""
        if experiment_id in self.active_experiments:
            experiment = self.active_experiments[experiment_id]
            if experiment.status == ExperimentStatus.RUNNING:
                measurement = ExperimentMeasurement(
                    name=measurement_name,
                    value=value,
                    timestamp=timestamp or datetime.now(),
                    raw_data=raw_data
                )
                experiment.measurements.append(measurement)
                
                # Check if experiment should be completed
                if self._should_complete_experiment(experiment):
                    self._complete_experiment(experiment)
                
                return True
        return False
    
    def _should_complete_experiment(self, experiment: Experiment) -> bool:
        """Check if experiment has enough data to complete"""
        if not experiment.end_date:
            return False
        
        # Complete if past end date or has minimum measurements
        return (datetime.now() >= experiment.end_date or 
                len(experiment.measurements) >= 10)  # Minimum data points
    
    def _complete_experiment(self, experiment: Experiment):
        """Complete experiment and analyze results"""
        experiment.status = ExperimentStatus.COMPLETED
        
        # Analyze results (simplified)
        if experiment.measurements:
            avg_value = sum(m.value for m in experiment.measurements) / len(experiment.measurements)
            experiment.success = avg_value > 0  # Simplified success criteria
            experiment.outcome = f"Average measurement: {avg_value:.2f}"
        else:
            experiment.success = False
            experiment.outcome = "Insufficient data collected"
        
        # Move to completed experiments
        self.completed_experiments.append(experiment)
        if experiment.id in self.active_experiments:
            del self.active_experiments[experiment.id]
    
    def get_experiment_results(self) -> List[Dict]:
        """Get results from successful experiments"""
        return [
            {
                "id": exp.id,
                "hypothesis": exp.hypothesis,
                "outcome": exp.outcome,
                "success": exp.success,
                "measurements_count": len(exp.measurements),
                "duration_days": (exp.end_date - exp.start_date).days if exp.start_date and exp.end_date else 0
            }
            for exp in self.completed_experiments
            if exp.success
        ]
    
    def get_active_experiments(self) -> List[Dict]:
        """Get currently active experiments"""
        return [
            {
                "id": exp.id,
                "hypothesis": exp.hypothesis,
                "status": exp.status.value,
                "measurements_count": len(exp.measurements),
                "days_running": (datetime.now() - exp.start_date).days if exp.start_date else 0
            }
            for exp in self.active_experiments.values()
        ]
