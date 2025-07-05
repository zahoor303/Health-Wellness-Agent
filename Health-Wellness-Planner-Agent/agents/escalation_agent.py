"""
Escalation Agent - Handles human coach requests
"""
from typing import Dict, Any
from context import RunContextWrapper
from hooks import hook_manager

class EscalationAgent:
    """Agent for escalating to human coaches"""
    
    def __init__(self):
        self.name = "escalation_agent"
    
    def handle_escalation(self, context: RunContextWrapper, reason: str = "general") -> Dict[str, Any]:
        """Handle escalation to human coach"""
        hook_manager.log_handoff("main_agent", self.name)
        
        # Log handoff
        context.get_context().add_handoff_log(f"Escalated to human coach: {reason}")
        
        # Prepare user summary
        user_summary = self.prepare_user_summary(context)
        
        return {
            "response_type": "escalation",
            "content": {
                "message": "I'll connect you with a human coach right away!",
                "escalation_reason": reason,
                "user_summary": user_summary,
                "next_steps": [
                    "Your request has been sent to our coaching team",
                    "A certified trainer will contact you within 24 hours",
                    "You can continue using the app while you wait"
                ],
                "estimated_wait_time": "24 hours"
            }
        }
    
    def prepare_user_summary(self, context: RunContextWrapper) -> Dict[str, Any]:
        """Prepare user summary for coach"""
        user_context = context.get_context()
        
        return {
            "user_name": user_context.name,
            "primary_goal": user_context.goal,
            "dietary_preferences": user_context.diet_preferences,
            "workout_plan": user_context.workout_plan,
            "progress_entries": len(user_context.progress_logs)
        }