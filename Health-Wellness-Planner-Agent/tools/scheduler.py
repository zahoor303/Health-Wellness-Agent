"""
Check-in Scheduler Tool
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from context import RunContextWrapper
from hooks import hook_manager

class CheckinSchedulerTool:
    """Tool for scheduling check-ins"""
    
    def __init__(self):
        self.name = "checkin_scheduler"
    
    def schedule_checkin(self, frequency: str, context: RunContextWrapper) -> Dict[str, Any]:
        """Schedule check-ins"""
        hook_manager.log_tool_start(self.name)
        
        try:
            # Parse frequency
            frequency_days = self.parse_frequency(frequency)
            
            # Create schedule
            schedule = self.create_schedule(frequency_days, context)
            
            # Update context
            context.get_context().add_progress_log("scheduling", f"Scheduled {frequency} check-ins")
            
            return {
                "response_type": "schedule",
                "content": {
                    "message": f"Great! I've scheduled {frequency} check-ins for you.",
                    "schedule": schedule,
                    "next_checkin": schedule["next_checkin"]
                }
            }
            
        except Exception as e:
            return {
                "response_type": "error",
                "content": {"error": str(e)}
            }
    
    def parse_frequency(self, frequency: str) -> int:
        """Parse frequency to days"""
        if "daily" in frequency.lower():
            return 1
        elif "weekly" in frequency.lower():
            return 7
        else:
            return 7  # Default weekly
    
    def create_schedule(self, frequency_days: int, context: RunContextWrapper) -> Dict[str, Any]:
        """Create check-in schedule"""
        current_date = datetime.now()
        
        # Generate next few check-in dates
        checkin_dates = []
        for i in range(4):
            next_checkin = current_date + timedelta(days=frequency_days * (i + 1))
            checkin_dates.append({
                "date": next_checkin.strftime("%Y-%m-%d"),
                "day": next_checkin.strftime("%A")
            })
        
        # Create questions
        questions = self.generate_questions(context)
        
        return {
            "frequency_days": frequency_days,
            "next_checkin": checkin_dates[0],
            "upcoming_checkins": checkin_dates,
            "questions": questions
        }
    
    def generate_questions(self, context: RunContextWrapper) -> List[str]:
        """Generate check-in questions"""
        base_questions = [
            "How are you feeling about your progress?",
            "Did you stick to your meal plan?",
            "How many workouts did you complete?",
            "What challenges did you face?",
            "What went well this week?"
        ]
        
        # Add goal-specific questions
        goal = context.get_context().goal
        if goal and goal.get('goal_type') == 'weight_loss':
            base_questions.append("Have you recorded your weight?")
        
        return base_questions