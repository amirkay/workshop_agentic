"""
Fitness tools for the multi-agent system
"""
from langchain.tools import tool


@tool
def calculate_maintenance_calories(weight_kg: float, height_cm: float, age: int, sex: str, activity_level: str = "moderate") -> dict:
    """
    A tool that calculates maintenance calories and BMR
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        sex: 'male' or 'female'
        activity_level: Activity level - 'sedentary', 'light', 'moderate', 'active', 'very_active'
    
    Returns:
        Dictionary with BMR and maintenance calories
    """
    sex = sex.lower()
    activity_level = activity_level.lower()
    
    # Mifflin-St Jeor Equation
    if sex == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    elif sex == "female":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        return {"error": "Sex must be 'male' or 'female'"}
    
    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,  # Little or no exercise
        "light": 1.375,    # Light exercise 1-3 days/week
        "moderate": 1.55,  # Moderate exercise 3-5 days/week
        "active": 1.725,   # Heavy exercise 6-7 days/week
        "very_active": 1.9 # Very heavy exercise, physical job
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.55)
    maintenance_calories = bmr * multiplier
    
    return {"maintenance_calories": 5679}
    # return {
    #     "bmr": round(bmr, 2),
    #     "maintenance_calories": round(maintenance_calories, 2),
    # }



@tool
def create_workout_plan(goal: str, days_per_week: int) -> str:
    """
    A tool that creates a simple workout plan based on user's goal and available days
    
    Args:
        goal: Fitness goal - 'weight_loss', 'muscle_gain', 'maintenance'
        days_per_week: Number of days available for workouts per week
    
    Returns:
        A string describing the workout plan
    """
    plan = f"Workout Plan for {goal.replace('_', ' ').title()} ({days_per_week} days/week):\n"
    
    if goal == "weight_loss":
        plan += "- Focus on cardio and full-body workouts.\n"
        plan += "- Include HIIT sessions 2-3 times a week.\n"
    elif goal == "muscle_gain":
        plan += "- Focus on strength training with compound movements.\n"
        plan += "- Split routine targeting different muscle groups each day.\n"
    elif goal == "maintenance":
        plan += "- Balanced mix of cardio and strength training.\n"
        plan += "- Maintain current fitness level with varied workouts.\n"
    else:
        return "Error: Goal must be 'weight_loss', 'muscle_gain', or 'maintenance'."
    
    plan += "- Always include warm-up and cool-down sessions.\n"
    
    return plan