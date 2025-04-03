from pydantic import BaseModel, Field
from typing import List, Optional

class UserPreferences(BaseModel):
    """Optional user preferences."""
    cuisine_types: Optional[List[str]] = Field(default_factory=list, description="Preferred cuisine types")
    complexity: Optional[str] = Field(default=None, description="Desired meal complexity (e.g., simple, medium, complex)")
    cook_time_limit_minutes: Optional[int] = Field(default=None, description="Maximum cooking time per meal in minutes")

class UserProfile(BaseModel):
    """Represents the user's profile for meal planning."""
    # user_id: str # Optional: Add if persistence is needed later
    dietary_restrictions: List[str] = Field(default_factory=list, description="e.g., vegetarian, vegan, gluten-free, keto")
    allergies: List[str] = Field(default_factory=list, description="List of ingredients the user is allergic to")
    dislikes: List[str] = Field(default_factory=list, description="List of ingredients the user dislikes")
    goals: List[str] = Field(default_factory=list, description="e.g., weight loss, muscle gain, general health")
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    target_calories: Optional[int] = Field(default=None, description="Optional target daily calorie intake")

    # Example usage:
    # profile = UserProfile(
    #     dietary_restrictions=["vegetarian"],
    #     allergies=["peanuts"],
    #     dislikes=["olives"],
    #     goals=["general health"],
    #     target_calories=2000,
    #     preferences=UserPreferences(cuisine_types=["italian"])
    # )

class Meal(BaseModel):
    """Represents a single meal within the plan."""
    meal_name: str
    recipe: str # Could be detailed steps or a summary

class DailyPlan(BaseModel):
    """Represents the meal plan for a single day."""
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    snacks: Optional[Meal] = None # Optional snacks

class MealPlan(BaseModel):
    """Represents the full 7-day meal plan."""
    monday: DailyPlan
    tuesday: DailyPlan
    wednesday: DailyPlan
    thursday: DailyPlan
    friday: DailyPlan
    saturday: DailyPlan
    sunday: DailyPlan
