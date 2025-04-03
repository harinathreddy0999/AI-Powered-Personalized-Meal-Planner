import streamlit as st
from models import UserProfile, UserPreferences, MealPlan, DailyPlan, Meal
from meal_generator import generate_meal_plan
from typing import List

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Personalized Meal Planner", layout="wide")

st.title(" Personalized Meal Planner ")
st.caption("Enter your details below and get a customized 7-day meal plan!")

# --- Helper function to display the plan ---
def display_meal_plan(plan: MealPlan):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for day_name in days:
        day_plan: DailyPlan = getattr(plan, day_name)
        with st.expander(f"**{day_name.capitalize()}**", expanded=False):
            st.subheader("Breakfast")
            st.markdown(f"**{day_plan.breakfast.meal_name}**")
            st.markdown(f"*Recipe:*\n{day_plan.breakfast.recipe}")

            st.subheader("Lunch")
            st.markdown(f"**{day_plan.lunch.meal_name}**")
            st.markdown(f"*Recipe:*\n{day_plan.lunch.recipe}")

            st.subheader("Dinner")
            st.markdown(f"**{day_plan.dinner.meal_name}**")
            st.markdown(f"*Recipe:*\n{day_plan.dinner.recipe}")

            if day_plan.snacks:
                st.subheader("Snacks (Optional)")
                st.markdown(f"**{day_plan.snacks.meal_name}**")
                st.markdown(f"*Recipe:*\n{day_plan.snacks.recipe}")

# --- User Input Form ---
st.header("Your Profile")

# Using columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Restrictions & Allergies")
    # Using text_input for flexibility, user enters comma-separated values
    dietary_restrictions_input = st.text_input("Dietary Restrictions (comma-separated, e.g., vegetarian, gluten-free)")
    allergies_input = st.text_input("Allergies (comma-separated, e.g., peanuts, shellfish)")
    dislikes_input = st.text_input("Dislikes (comma-separated, e.g., mushrooms, olives)")

with col2:
    st.subheader("Goals & Preferences")
    goals_input = st.text_input("Health/Fitness Goals (comma-separated, e.g., weight loss, muscle gain)")
    target_calories = st.number_input("Target Daily Calories (Optional)", min_value=0, step=100, value=None)
    cuisine_types_input = st.text_input("Preferred Cuisines (comma-separated, Optional)")
    complexity = st.selectbox("Desired Meal Complexity (Optional)", ["Any", "Simple", "Medium", "Complex"], index=0)
    cook_time_limit = st.number_input("Max Cook Time per Meal (minutes, Optional)", min_value=0, step=15, value=None)

# Helper to parse comma-separated input
def parse_list_input(input_string: str) -> List[str]:
    return [item.strip() for item in input_string.split(',') if item.strip()]

# --- Generate Button and Output ---
st.divider()

if st.button("Generate Meal Plan", type="primary"):
    # Basic input validation example (can be expanded)
    if not dietary_restrictions_input and not allergies_input and not dislikes_input and not goals_input:
         st.warning("Please fill in at least one profile field to get a personalized plan.")
    else:
        # Create UserProfile from inputs
        user_profile = UserProfile(
            dietary_restrictions=parse_list_input(dietary_restrictions_input),
            allergies=parse_list_input(allergies_input),
            dislikes=parse_list_input(dislikes_input),
            goals=parse_list_input(goals_input),
            target_calories=target_calories if target_calories and target_calories > 0 else None,
            preferences=UserPreferences(
                cuisine_types=parse_list_input(cuisine_types_input),
                complexity=complexity if complexity != "Any" else None,
                cook_time_limit_minutes=cook_time_limit if cook_time_limit and cook_time_limit > 0 else None
            )
        )

        st.subheader("Generating your plan...")
        st.write("Profile being used:")
        st.json(user_profile.model_dump_json(indent=2)) # Show the profile being sent

        with st.spinner("Calling the AI chef... Please wait."):
            # Call the generation function
            meal_plan = generate_meal_plan(user_profile)

        if meal_plan:
            st.success("Your 7-Day Meal Plan is Ready!")
            display_meal_plan(meal_plan)
        else:
            st.error("Sorry, something went wrong while generating the meal plan. Please check the console logs or ensure your API key is set correctly in the .env file and try again.")
            st.info("Common issues: Missing API key, invalid API key, LLM API errors, or the LLM failed to return valid JSON.")

st.sidebar.info(
    """
    **How to Use:**
    1. Fill in your dietary needs, goals, and preferences.
    2. Click 'Generate Meal Plan'.
    3. Wait for the AI to create your custom plan.

    **Note:** Requires an OpenAI or Anthropic API key set in a `.env` file in the app directory.
    Create a file named `.env` and add `OPENAI_API_KEY='your_key'` or `ANTHROPIC_API_KEY='your_key'`.
    """
)
