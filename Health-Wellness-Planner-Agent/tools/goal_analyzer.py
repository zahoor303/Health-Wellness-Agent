"""
Goal Analyzer Tool
"""
from typing import Dict, Any
from context import RunContextWrapper
from guardrails import GuardrailValidator
from hooks import hook_manager

class GoalAnalyzerTool:
    """Tool for analyzing user goals"""
    
    def __init__(self):
        self.name = "goal_analyzer"
    
    def analyze_goal(self, goal_text: str, context: RunContextWrapper) -> Dict[str, Any]:
        """Analyze user goal"""
        hook_manager.log_tool_start(self.name)
        
        try:
            # Validate input
            goal_data = GuardrailValidator.validate_goal_input(goal_text)
            if not isinstance(goal_data, dict):
                goal_data = {"original_text": goal_text}
            
            # Update context
            context.update_context(goal=goal_data)
            context.get_context().add_progress_log("goal_analysis", f"Set goal: {goal_text}")
            
            # Analyze feasibility
            feasibility = self.analyze_feasibility(goal_data)
            
            response = {
                "response_type": "goal_analysis",
                "content": {
                    "message": f"Great! I've analyzed your goal: {goal_text}",
                    "goal_data": goal_data,
                    "feasibility": feasibility,
                    "recommendations": [
                        "Start with small, consistent changes",
                        "Track your progress regularly",
                        "Stay hydrated and get enough sleep"
                    ]
                }
            }
            
            return GuardrailValidator.validate_output(response)
            
        except Exception as e:
            return {
                "response_type": "error",
                "content": {"error": str(e)}
            }
    
    def analyze_feasibility(self, goal_data: Dict[str, Any]) -> str:
        """Analyze if goal is feasible"""
        if goal_data['goal_type'] == 'weight_loss':
            if goal_data['quantity'] and goal_data['quantity'] > 2:
                return "challenging but achievable"
            else:
                return "very achievable"
        else:
            return "achievable with consistency"