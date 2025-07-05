"""
Progress Tracker Tool
"""
from typing import Dict, Any, List
from datetime import datetime
from context import RunContextWrapper
from hooks import hook_manager

class ProgressTrackerTool:
    """Tool for tracking progress"""
    
    def __init__(self):
        self.name = "progress_tracker"
    
    def update_progress(self, progress_data: Dict[str, Any], context: RunContextWrapper) -> Dict[str, Any]:
        """Update progress"""
        hook_manager.log_tool_start(self.name)
        
        try:
            # Validate progress data
            validated_data = self.validate_progress(progress_data)
            
            # Update context
            self.update_context_with_progress(validated_data, context)
            
            # Analyze progress
            analysis = self.analyze_progress(validated_data, context)
            
            return {
                "response_type": "progress_update",
                "content": {
                    "message": "Progress updated successfully!",
                    "progress_data": validated_data,
                    "analysis": analysis,
                    "recommendations": self.generate_recommendations(analysis)
                }
            }
            
        except Exception as e:
            return {
                "response_type": "error",
                "content": {"error": str(e)}
            }
    
    def validate_progress(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate progress data"""
        validated = {
            "timestamp": datetime.now().isoformat(),
            "notes": data.get("notes", ""),
            "metrics": {}
        }
        
        # Extract metrics
        if "weight" in data:
            validated["metrics"]["weight"] = float(data["weight"])
        
        if "workouts_completed" in data:
            validated["metrics"]["workouts_completed"] = int(data["workouts_completed"])
        
        return validated
    
    def update_context_with_progress(self, progress_data: Dict[str, Any], context: RunContextWrapper):
        """Update context with progress"""
        import json
        context.get_context().add_progress_log("progress_update", json.dumps(progress_data))
    
    def analyze_progress(self, progress_data: Dict[str, Any], context: RunContextWrapper) -> Dict[str, Any]:
        """Analyze progress"""
        analysis = {
            "overall_score": 75,  # Default score
            "insights": []
        }
        
        # Analyze workout completion
        workouts = progress_data.get("metrics", {}).get("workouts_completed", 0)
        if workouts >= 3:
            analysis["insights"].append("Great job on workout consistency!")
        elif workouts >= 1:
            analysis["insights"].append("Good start! Try to increase workout frequency.")
        else:
            analysis["insights"].append("Let's work on getting more workouts in.")
        
        return analysis
    
    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations"""
        recommendations = [
            "Keep tracking your progress regularly",
            "Stay consistent with your plan",
            "Celebrate small wins"
        ]
        
        if analysis["overall_score"] < 50:
            recommendations.append("Consider adjusting your goals to be more achievable")
        
        return recommendations