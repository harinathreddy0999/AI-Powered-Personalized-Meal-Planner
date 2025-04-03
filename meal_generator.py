import os
import json
from typing import Optional # Import Optional for type hinting
from dotenv import load_dotenv
from openai import OpenAI # Or import Anthropic, etc.
from models import UserProfile, MealPlan # Import our Pydantic models

# Load environment variables (API key)
load_dotenv()

# --- Option 1: OpenAI Client ---
# Make sure OPENAI_API_KEY is set in your .env file
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# MODEL_NAME = "gpt-3.5-turbo" # Or "gpt-4" etc.

# --- Option 2: Anthropic Client (Example) ---
# from anthropic import Anthropic
# Make sure ANTHROPIC_API_KEY is set in your .env file
# client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# MODEL_NAME = "claude-3-sonnet-20240229" # Or other Claude models

# --- Select and Configure Client ---
# For this example, let's assume OpenAI for now. Uncomment/modify as needed.
# Import OpenAIError specifically for better handling
from openai import OpenAIError

client = None
MODEL_NAME = None

try:
    # Attempt to initialize OpenAI client
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        # Don't even try to initialize if the key is clearly missing from env
        raise ValueError("OpenAI API key not found in environment variables. Please set OPENAI_API_KEY in .env file.")

    client = OpenAI(api_key=openai_api_key)
    # If the constructor succeeds, the key is at least present.
    # A basic check like pinging models might be needed for full validation, but is often overkill here.
    MODEL_NAME = "gpt-3.5-turbo"
    print("Attempting to use OpenAI client.") # Changed message slightly

except (ImportError, ValueError, OpenAIError) as e:
    # Catch missing library, explicitly missing key, or initialization errors (like invalid key)
    print(f"OpenAI Client Error: {e}")
    print("Falling back to check for Anthropic client...")
    client = None # Ensure client is None if OpenAI fails
    MODEL_NAME = None

    # --- Option 2: Anthropic Client (Fallback) ---
    try:
        # Try importing Anthropic first
        from anthropic import Anthropic, AnthropicError

        # If import succeeds, proceed with initialization
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_api_key:
             raise ValueError("Anthropic API key not found in environment variables. Please set ANTHROPIC_API_KEY in .env file.")

        client = Anthropic(api_key=anthropic_api_key)
        MODEL_NAME = "claude-3-sonnet-20240229"
        print("Using Anthropic client.")

    except ImportError:
        # Handle case where anthropic library is not installed
        print("Anthropic library not found. Skipping Anthropic client.")
        # client and MODEL_NAME remain None from the previous block
    except (ValueError, AnthropicError) as anthropic_e:
        # Handle errors only if import succeeded but initialization failed (missing/invalid key)
        print(f"Anthropic Client Error: {anthropic_e}")
        client = None # Ensure client is None
        MODEL_NAME = None
    except Exception as general_e:
        # Catch any other unexpected errors during Anthropic setup
        print(f"Unexpected error during Anthropic setup: {general_e}")
        client = None
        MODEL_NAME = None

# Final check if any client was successfully initialized
if client:
    print(f"Successfully initialized LLM client: {type(client).__name__} with model {MODEL_NAME}")
else:
    # This message now correctly reflects that neither client could be set up
    print("Warning: No LLM client initialized. Please ensure at least one API key (OpenAI or Anthropic) is correctly set in the .env file and the corresponding library is installed.")

# Final check if any client was successfully initialized
if client:
    print(f"Successfully initialized LLM client: {type(client).__name__} with model {MODEL_NAME}")
else:
    print("Warning: No LLM client initialized. Meal generation will not work.")


def build_llm_prompt(profile: UserProfile) -> str:
    """Constructs the prompt for the LLM based on the user profile."""
    prompt = f"Generate a personalized 7-day meal plan (Monday to Sunday) for a user with the following profile:\n"
    prompt += f"- Dietary Restrictions: {', '.join(profile.dietary_restrictions) if profile.dietary_restrictions else 'None'}\n"
    prompt += f"- Allergies: {', '.join(profile.allergies) if profile.allergies else 'None'}\n"
    prompt += f"- Dislikes: {', '.join(profile.dislikes) if profile.dislikes else 'None'}\n"
    prompt += f"- Goals: {', '.join(profile.goals) if profile.goals else 'None specified'}\n"
    if profile.target_calories:
        prompt += f"- Target Daily Calories: Approximately {profile.target_calories} kcal\n"
    if profile.preferences.cuisine_types:
        prompt += f"- Preferred Cuisines: {', '.join(profile.preferences.cuisine_types)}\n"
    if profile.preferences.complexity:
        prompt += f"- Desired Complexity: {profile.preferences.complexity}\n"
    if profile.preferences.cook_time_limit_minutes:
        prompt += f"- Max Cook Time Per Meal: {profile.preferences.cook_time_limit_minutes} minutes\n"

    prompt += "\nPlease provide a plan including Breakfast, Lunch, and Dinner for each day."
    prompt += " For each meal, provide a 'meal_name' and a 'recipe' with simple, easy-to-follow instructions."
    prompt += " Ensure the plan strictly adheres to all dietary restrictions, allergies, and dislikes."
    prompt += " Structure the output as a valid JSON object following this Pydantic model structure:\n"
    prompt += f"```json\n{MealPlan.model_json_schema(indent=2)}\n```\n"
    prompt += "Ensure the final output is ONLY the JSON object, without any introductory text or explanations."

    return prompt

def generate_meal_plan(profile: UserProfile) -> Optional[MealPlan]:
    """Generates a meal plan using the LLM based on the user profile."""
    if not client or not MODEL_NAME:
         print("LLM client not initialized. Cannot generate plan.")
         return None # Or raise an error

    prompt = build_llm_prompt(profile)
    print("\n--- Sending Prompt to LLM ---")
    # print(prompt) # Uncomment to debug the prompt
    print("---------------------------\n")

    try:
        if isinstance(client, OpenAI):
            # OpenAI API Call
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful meal planning assistant. Generate meal plans in JSON format based on user profiles."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}, # Request JSON output if using compatible models
                temperature=0.7, # Adjust creativity vs. determinism
            )
            raw_json_output = response.choices[0].message.content

        elif 'Anthropic' in str(type(client)): # Check if it's an Anthropic client
             # Anthropic API Call (Example)
             message = client.messages.create(
                 model=MODEL_NAME,
                 max_tokens=4000, # Adjust as needed
                 system="You are a helpful meal planning assistant. Generate meal plans strictly in the requested JSON format based on user profiles. Output ONLY the JSON object.",
                 messages=[
                     {"role": "user", "content": prompt}
                 ]
             )
             raw_json_output = message.content[0].text
        else:
             print("Unsupported LLM client type.")
             return None


        print("\n--- Received Raw LLM Output ---")
        # print(raw_json_output) # Uncomment to debug raw output
        print("-----------------------------\n")

        # Attempt to parse the JSON output
        try:
            plan_data = json.loads(raw_json_output)
            # Validate the parsed data against the Pydantic model
            meal_plan = MealPlan(**plan_data)
            print("Successfully parsed and validated meal plan.")
            return meal_plan
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode LLM response as JSON: {e}")
            print("--- Raw Output causing error ---")
            print(raw_json_output)
            print("-------------------------------")
            return None
        except Exception as e: # Catch Pydantic validation errors etc.
            print(f"Error: Failed to validate meal plan structure: {e}")
            print("--- Parsed Data causing error ---")
            try:
                print(json.dumps(plan_data, indent=2))
            except NameError: # If json.loads failed earlier
                 print(raw_json_output)
            print("--------------------------------")
            return None

    except Exception as e:
        print(f"Error during LLM API call: {e}")
        return None

# Example usage (for testing)
if __name__ == "__main__":
    # Create a sample profile
    test_profile = UserProfile(
        dietary_restrictions=["vegetarian", "gluten-free"],
        allergies=["peanuts"],
        dislikes=["mushrooms", "olives"],
        goals=["weight loss"],
        target_calories=1800,
        preferences=UserPreferences(cuisine_types=["italian", "mexican"], complexity="simple")
    )

    print("Generating test meal plan...")
    generated_plan = generate_meal_plan(test_profile)

    if generated_plan:
        print("\n--- Generated Meal Plan (JSON) ---")
        print(generated_plan.model_dump_json(indent=2))
        print("----------------------------------")
    else:
        print("\nFailed to generate meal plan.")
