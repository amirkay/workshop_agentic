"""
Fitness tools for the multi-agent system
"""
from langchain.tools import tool


@tool
def calculate_maintenance_calories(weight_kg: float, height_cm: float, age: int, sex: str, activity_level: str = "moderate") -> dict:
    """
    Calculate maintenance calories using the Mifflin-St Jeor equation.
    
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
    
    return {
        "bmr": round(bmr, 2),
        "maintenance_calories": round(maintenance_calories, 2),
        "activity_level": activity_level,
        "weight_kg": weight_kg,
        "height_cm": height_cm,
        "age": age,
        "sex": sex
    }

