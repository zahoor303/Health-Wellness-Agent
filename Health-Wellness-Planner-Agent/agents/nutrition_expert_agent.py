"""
Nutrition Expert Agent - Handles complex dietary needs
"""
from typing import Dict, Any, List
from context import RunContextWrapper
from hooks import hook_manager

class NutritionExpertAgent:
    """Agent for nutrition expertise"""
    
    def __init__(self):
        self.name = "nutrition_expert_agent"
    
    def handle_nutrition_consultation(self, context: RunContextWrapper, consultation_type: str = "general") -> Dict[str, Any]:
        """Handle nutrition consultation"""
        hook_manager.log_handoff("main_agent", self.name)
        
        # Log handoff
        context.get_context().add_handoff_log(f"Nutrition consultation: {consultation_type}")
        
        # Generate recommendations
        recommendations = self.generate_recommendations(consultation_type)
        
        return {
            "response_type": "nutrition_consultation",
            "content": {
                "message": "I'm here to help with your specialized nutrition needs.",
                "consultation_type": consultation_type,
                "recommendations": recommendations,
                "important_notes": self.get_important_notes(consultation_type),
                "resources": self.get_resources(consultation_type)
            }
        }
    
    def generate_recommendations(self, consultation_type: str) -> List[Dict[str, Any]]:
        """Generate nutrition recommendations"""
        if consultation_type == "diabetes":
            return [
                {
                    "category": "carbohydrate_management",
                    "priority": "high",
                    "recommendation": "Focus on complex carbohydrates and monitor portions",
                    "reason": "Helps maintain stable blood glucose"
                },
                {
                    "category": "fiber_intake",
                    "priority": "high",
                    "recommendation": "Include 25-35g fiber daily",
                    "reason": "Slows glucose absorption"
                }
            ]
        elif consultation_type == "allergies":
            return [
                {
                    "category": "allergen_avoidance",
                    "priority": "high",
                    "recommendation": "Read all food labels carefully",
                    "reason": "Prevent allergic reactions"
                },
                {
                    "category": "nutrient_replacement",
                    "priority": "medium",
                    "recommendation": "Find alternative nutrient sources",
                    "reason": "Maintain nutritional adequacy"
                }
            ]
        else:
            return [
                {
                    "category": "general_nutrition",
                    "priority": "medium",
                    "recommendation": "Eat a balanced diet with variety",
                    "reason": "Ensures adequate nutrition"
                }
            ]
    
    def get_important_notes(self, consultation_type: str) -> List[str]:
        """Get important notes"""
        notes = [
            "This advice is for educational purposes only",
            "Always consult with a healthcare provider",
            "Individual needs may vary"
        ]
        
        if consultation_type == "diabetes":
            notes.append("Monitor blood glucose levels regularly")
        elif consultation_type == "allergies":
            notes.append("Keep emergency medication available")
        
        return notes
    
    def get_resources(self, consultation_type: str) -> List[Dict[str, str]]:
        """Get educational resources"""
        return [
            {
                "title": "Nutrition Guidelines",
                "type": "article",
                "description": "Basic principles of healthy eating"
            },
            {
                "title": "Meal Planning Guide",
                "type": "guide",
                "description": "How to plan nutritious meals"
            }
        ]