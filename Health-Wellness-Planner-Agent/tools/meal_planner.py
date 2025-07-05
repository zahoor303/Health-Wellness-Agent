"""
Meal Planner Tool
"""
from typing import Dict, Any, List
from context import RunContextWrapper
from guardrails import GuardrailValidator
from hooks import hook_manager

class MealPlannerTool:
    """Tool for generating meal plans"""
    
    def __init__(self):
        self.name = "meal_planner"
    
    def generate_meal_plan(self, dietary_preferences: str, goal: Dict[str, Any], context: RunContextWrapper) -> Dict[str, Any]:
        """Generate 7-day meal plan"""
        hook_manager.log_tool_start(self.name)
        
        try:
            # Validate diet type
            diet_type = GuardrailValidator.validate_dietary_input(dietary_preferences)
            
            # Create meal plan
            meal_plan = self.create_meal_plan(diet_type, goal)
            
            # Update context
            context.update_context(
                diet_preferences=diet_type,
                meal_plan=meal_plan["daily_plans"]
            )
            context.get_context().add_progress_log("meal_planning", f"Generated {diet_type} meal plan")
            
            response = {
                "response_type": "meal_plan",
                "content": meal_plan
            }
            
            return GuardrailValidator.validate_output(response)
            
        except Exception as e:
            return {
                "response_type": "error",
                "content": {"error": str(e)}
            }
    
    def create_meal_plan(self, diet_type: str, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured meal plan"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Meal templates
        meal_templates = {
            "vegetarian": {
                "breakfast": ["Oatmeal with berries", "Veggie scramble", "Smoothie bowl", "Avocado toast"],
                "lunch": ["Quinoa salad", "Vegetable soup", "Caprese sandwich", "Buddha bowl"],
                "dinner": ["Pasta primavera", "Stuffed peppers", "Vegetable stir-fry", "Lentil curry"],
                "snack": ["Greek yogurt", "Mixed nuts", "Fruit", "Hummus with veggies"]
            },
            "vegan": {
                "breakfast": ["Chia pudding", "Smoothie bowl", "Oatmeal", "Avocado toast"],
                "lunch": ["Quinoa bowl", "Veggie wrap", "Salad", "Soup"],
                "dinner": ["Tofu stir-fry", "Lentil curry", "Vegetable pasta", "Buddha bowl"],
                "snack": ["Nuts", "Fruit", "Vegetables", "Plant yogurt"]
            },
            "keto": {
                "breakfast": ["Eggs and bacon", "Avocado", "Keto smoothie", "Cheese omelet"],
                "lunch": ["Chicken salad", "Zucchini noodles", "Keto bowl", "Lettuce wraps"],
                "dinner": ["Salmon", "Steak", "Chicken thighs", "Pork chops"],
                "snack": ["Cheese", "Nuts", "Olives", "Fat bombs"]
            },
            "omnivore": {
                "breakfast": ["Eggs", "Oatmeal", "Smoothie", "Toast"],
                "lunch": ["Chicken salad", "Sandwich", "Soup", "Bowl"],
                "dinner": ["Grilled chicken", "Fish", "Pasta", "Stir-fry"],
                "snack": ["Yogurt", "Fruit", "Nuts", "Vegetables"]
            }
        }
        
        templates = meal_templates.get(diet_type, meal_templates["omnivore"])
        
        daily_plans = []
        for i, day in enumerate(days):
            daily_plan = {
                "day": day,
                "meals": {
                    "breakfast": templates["breakfast"][i % len(templates["breakfast"])],
                    "lunch": templates["lunch"][i % len(templates["lunch"])],
                    "dinner": templates["dinner"][i % len(templates["dinner"])],
                    "snack": templates["snack"][i % len(templates["snack"])]
                },
                "calories": self.estimate_calories(goal)
            }
            daily_plans.append(daily_plan)
        
        return {
            "dietary_type": diet_type,
            "daily_plans": daily_plans,
            "tips": self.get_tips(diet_type)
        }
    
    def estimate_calories(self, goal: Dict[str, Any]) -> int:
        """Estimate daily calories"""
        base_calories = 2000
        
        if goal.get("goal_type") == "weight_loss":
            return base_calories - 300
        elif goal.get("goal_type") == "weight_gain":
            return base_calories + 300
        else:
            return base_calories
    
    def get_tips(self, diet_type: str) -> List[str]:
        """Get dietary tips"""
        tips = {
            "vegetarian": ["Include protein with each meal", "Take B12 supplements"],
            "vegan": ["Combine proteins", "Take B12 and D3 supplements"],
            "keto": ["Monitor ketones", "Stay hydrated"],
            "omnivore": ["Eat variety", "Include fruits and vegetables"]
        }
        
        return tips.get(diet_type, ["Eat balanced meals", "Stay hydrated"])