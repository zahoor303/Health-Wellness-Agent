"""
Main Health & Wellness Planner Agent
"""
from typing import Dict, Any
from context import RunContextWrapper
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool
from tools.scheduler import CheckinSchedulerTool
from tools.tracker import ProgressTrackerTool
from agents.escalation_agent import EscalationAgent
from agents.nutrition_expert_agent import NutritionExpertAgent
from agents.injury_support_agent import InjurySupportAgent

class HealthWellnessAgent:
    """Main Health & Wellness Planner Agent"""
    
    def __init__(self):
        self.name = "Health & Wellness Planner"
        
        # Initialize tools
        self.tools = {
            'goal_analyzer': GoalAnalyzerTool(),
            'meal_planner': MealPlannerTool(),
            'workout_recommender': WorkoutRecommenderTool(),
            'checkin_scheduler': CheckinSchedulerTool(),
            'progress_tracker': ProgressTrackerTool()
        }
        
        # Initialize specialized agents
        self.agents = {
            'escalation_agent': EscalationAgent(),
            'nutrition_expert_agent': NutritionExpertAgent(),
            'injury_support_agent': InjurySupportAgent()
        }
    
    def process_message(self, message: str, context: RunContextWrapper) -> Dict[str, Any]:
        """Process user message and return response"""
        
        # Determine what the user wants
        intent = self.get_intent(message)
        
        # Check for handoff first
        handoff_agent = self.check_handoff(message)
        if handoff_agent:
            return self.handle_handoff(handoff_agent, message, context)
        
        # Use appropriate tool
        if intent == 'goal':
            return self.tools['goal_analyzer'].analyze_goal(message, context)
        elif intent == 'meal':
            diet_type = self.extract_diet_type(message)
            goal = context.get_context().goal or {}
            return self.tools['meal_planner'].generate_meal_plan(diet_type, goal, context)
        elif intent == 'workout':
            goal = context.get_context().goal or {}
            return self.tools['workout_recommender'].recommend_workout(message, goal, context)
        elif intent == 'progress':
            progress_data = self.extract_progress_data(message)
            return self.tools['progress_tracker'].update_progress(progress_data, context)
        elif intent == 'schedule':
            frequency = self.extract_frequency(message)
            return self.tools['checkin_scheduler'].schedule_checkin(frequency, context)
        else:
            return self.handle_general_conversation(message)
    
    def get_intent(self, message: str) -> str:
        """Determine user intent from message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['goal', 'want to', 'trying to']):
            return 'goal'
        elif any(word in message_lower for word in ['meal', 'food', 'diet', 'eat']):
            return 'meal'
        elif any(word in message_lower for word in ['workout', 'exercise', 'fitness']):
            return 'workout'
        elif any(word in message_lower for word in ['progress', 'update', 'track']):
            return 'progress'
        elif any(word in message_lower for word in ['schedule', 'remind', 'checkin']):
            return 'schedule'
        else:
            return 'general'
    
    def check_handoff(self, message: str) -> str:
        """Check if we need to handoff to specialist"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['human', 'coach', 'trainer', 'person']):
            return 'escalation_agent'
        elif any(word in message_lower for word in ['diabetes', 'allergy', 'allergic']):
            return 'nutrition_expert_agent'
        elif any(word in message_lower for word in ['injury', 'pain', 'hurt']):
            return 'injury_support_agent'
        
        return None
    
    def handle_handoff(self, agent_name: str, message: str, context: RunContextWrapper) -> Dict[str, Any]:
        """Handle handoff to specialized agent"""
        agent = self.agents[agent_name]
        
        if agent_name == 'escalation_agent':
            return agent.handle_escalation(context, message)
        elif agent_name == 'nutrition_expert_agent':
            consultation_type = self.extract_nutrition_type(message)
            return agent.handle_nutrition_consultation(context, consultation_type)
        elif agent_name == 'injury_support_agent':
            injury_type = self.extract_injury_type(message)
            return agent.handle_injury_consultation(context, injury_type)
    
    def extract_diet_type(self, message: str) -> str:
        """Extract diet type from message"""
        message_lower = message.lower()
        
        if 'vegetarian' in message_lower:
            return 'vegetarian'
        elif 'vegan' in message_lower:
            return 'vegan'
        elif 'keto' in message_lower:
            return 'keto'
        else:
            return 'omnivore'
    
    def extract_nutrition_type(self, message: str) -> str:
        """Extract nutrition consultation type"""
        message_lower = message.lower()
        
        if 'diabetes' in message_lower:
            return 'diabetes'
        elif 'allergy' in message_lower:
            return 'allergies'
        else:
            return 'general'
    
    def extract_injury_type(self, message: str) -> str:
        """Extract injury type"""
        message_lower = message.lower()
        
        if 'knee' in message_lower:
            return 'knee'
        elif 'back' in message_lower:
            return 'back'
        elif 'shoulder' in message_lower:
            return 'shoulder'
        else:
            return 'general'
    
    def extract_progress_data(self, message: str) -> Dict[str, Any]:
        """Extract progress data from message"""
        import re
        
        data = {'notes': message}
        
        # Extract weight
        weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|lbs)', message.lower())
        if weight_match:
            data['weight'] = weight_match.group(1)
        
        # Extract workout count
        workout_match = re.search(r'(\d+)\s*workout', message.lower())
        if workout_match:
            data['workouts_completed'] = workout_match.group(1)
        
        return data
    
    def extract_frequency(self, message: str) -> str:
        """Extract frequency from message"""
        message_lower = message.lower()
        
        if 'daily' in message_lower:
            return 'daily'
        elif 'weekly' in message_lower:
            return 'weekly'
        else:
            return 'weekly'
    
    def handle_general_conversation(self, message: str) -> Dict[str, Any]:
        """Handle general conversation"""
        if any(word in message.lower() for word in ['help', 'what can you do']):
            return {
                'response_type': 'help',
                'content': {
                    'message': "I'm your AI health and wellness assistant!",
                    'capabilities': [
                        "🎯 Set and analyze fitness goals",
                        "🍽️ Create personalized meal plans",
                        "💪 Design workout routines",
                        "📊 Track your progress",
                        "📅 Schedule check-ins",
                        "🏥 Connect with specialists"
                    ]
                }
            }
        
        return {
            'response_type': 'conversation',
            'content': {
                'message': "Hi! I can help you with your health and wellness goals. What would you like to work on today?",
                'suggestions': [
                    "Set a fitness goal",
                    "Get a meal plan",
                    "Create a workout routine",
                    "Track my progress"
                ]
            }
        }