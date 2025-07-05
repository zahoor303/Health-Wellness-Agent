"""
Injury Support Agent - Handles physical limitations
"""
from typing import Dict, Any, List
from context import RunContextWrapper
from hooks import hook_manager

class InjurySupportAgent:
    """Agent for injury support"""
    
    def __init__(self):
        self.name = "injury_support_agent"
    
    def handle_injury_consultation(self, context: RunContextWrapper, injury_type: str = "general") -> Dict[str, Any]:
        """Handle injury consultation"""
        hook_manager.log_handoff("main_agent", self.name)
        
        # Log handoff
        context.get_context().add_handoff_log(f"Injury consultation: {injury_type}")
        
        # Analyze injury
        injury_analysis = self.analyze_injury(injury_type)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(injury_type)
        
        # Create modified workout
        modified_plan = self.create_modified_workout(injury_type)
        
        # Update context
        context.update_context(injury_notes=f"{injury_type}: modified plan created")
        
        return {
            "response_type": "injury_consultation",
            "content": {
                "message": "I'll help you stay active safely while you recover.",
                "injury_type": injury_type,
                "injury_analysis": injury_analysis,
                "recommendations": recommendations,
                "modified_workout_plan": modified_plan,
                "safety_guidelines": self.get_safety_guidelines(injury_type)
            }
        }
    
    def analyze_injury(self, injury_type: str) -> Dict[str, Any]:
        """Analyze injury situation"""
        analysis = {
            "injury_type": injury_type,
            "severity": "moderate",
            "affected_areas": [],
            "safe_movements": [],
            "avoid_movements": []
        }
        
        if injury_type == "knee":
            analysis.update({
                "affected_areas": ["knee", "lower_leg"],
                "safe_movements": ["swimming", "upper_body_exercises"],
                "avoid_movements": ["jumping", "running", "deep_squats"]
            })
        elif injury_type == "back":
            analysis.update({
                "affected_areas": ["lower_back", "core"],
                "safe_movements": ["walking", "gentle_stretching"],
                "avoid_movements": ["heavy_lifting", "twisting"]
            })
        elif injury_type == "shoulder":
            analysis.update({
                "affected_areas": ["shoulder", "upper_arm"],
                "safe_movements": ["lower_body_exercises", "walking"],
                "avoid_movements": ["overhead_movements", "heavy_pressing"]
            })
        
        return analysis
    
    def generate_recommendations(self, injury_type: str) -> List[Dict[str, Any]]:
        """Generate injury-specific recommendations"""
        base_recommendations = [
            {
                "category": "general_safety",
                "priority": "high",
                "recommendation": "Listen to your body and stop if you feel pain",
                "reason": "Prevent further injury"
            },
            {
                "category": "recovery",
                "priority": "high",
                "recommendation": "Apply ice after activity if there's swelling",
                "reason": "Reduce inflammation"
            }
        ]
        
        if injury_type == "knee":
            base_recommendations.append({
                "category": "exercise_modification",
                "priority": "medium",
                "recommendation": "Focus on upper body and swimming",
                "reason": "Maintain fitness while protecting knee"
            })
        
        return base_recommendations
    
    def create_modified_workout(self, injury_type: str) -> Dict[str, Any]:
        """Create modified workout plan"""
        if injury_type == "knee":
            return {
                "weekly_plan": [
                    {"day": "Monday", "focus": "Upper Body", "exercises": ["Seated Shoulder Press", "Chest Press", "Seated Row"], "notes": "All seated exercises"},
                    {"day": "Wednesday", "focus": "Core", "exercises": ["Seated Core Twists", "Upper Body Stretches"], "notes": "Gentle movements only"},
                    {"day": "Friday", "focus": "Swimming", "exercises": ["Swimming", "Water Walking"], "notes": "Low-impact cardio"}
                ]
            }
        elif injury_type == "back":
            return {
                "weekly_plan": [
                    {"day": "Monday", "focus": "Gentle Movement", "exercises": ["Walking", "Gentle Stretches"], "notes": "Keep spine neutral"},
                    {"day": "Wednesday", "focus": "Core Stability", "exercises": ["Dead Bug", "Bird Dog"], "notes": "Focus on form"},
                    {"day": "Friday", "focus": "Lower Body", "exercises": ["Wall Squats", "Calf Raises"], "notes": "Avoid bending forward"}
                ]
            }
        else:
            return {
                "weekly_plan": [
                    {"day": "Monday", "focus": "Lower Body", "exercises": ["Squats", "Lunges"], "notes": "Avoid using injured area"},
                    {"day": "Wednesday", "focus": "Cardio", "exercises": ["Walking", "Stationary Bike"], "notes": "Low impact only"},
                    {"day": "Friday", "focus": "Flexibility", "exercises": ["Gentle Stretching"], "notes": "Pain-free range only"}
                ]
            }
    
    def get_safety_guidelines(self, injury_type: str) -> List[str]:
        """Get safety guidelines"""
        guidelines = [
            "Stop immediately if you experience sharp pain",
            "Progress gradually",
            "Consult healthcare provider if symptoms worsen"
        ]
        
        if injury_type == "knee":
            guidelines.append("Avoid deep squats and lunges")
        elif injury_type == "back":
            guidelines.append("Maintain neutral spine alignment")
        
        return guidelines