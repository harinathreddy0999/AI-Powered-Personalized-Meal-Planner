

# 🌟 AI-Powered Personalized Meal Planner 🥗🤖

## 🚀 Overview
Tired of generic meal plans? This AI-powered application generates a **customized 7-day meal plan** tailored to individual needs, making healthy eating simpler and more enjoyable.

### ✨ Key Features:
- ✅ **Robust Data Modeling with Pydantic**
- 💻 **Interactive UI with Streamlit**
- 🤖 **Intelligent Meal Generation via LLMs (GPT/Claude)**
- 📜 **Structured JSON Output & Validation**
- 🔄 **API Flexibility (Supports OpenAI & Anthropic)**

---

## 🏗️ Tech Stack
- **Python** 🐍
- **Pydantic** 📜 (For strict data validation)
- **Streamlit** 🖥️ (For an interactive UI)
- **OpenAI GPT & Anthropic Claude** 🤖 (For AI-powered meal generation)
- **dotenv** 🌎 (For secure API key management)

---

## 🛠️ Setup & Installation
### 🔹 1. Clone the Repository
```bash
 git clone https://github.com/your-repo/ai-meal-planner.git
 cd ai-meal-planner
```
### 🔹 2. Create a Virtual Environment & Install Dependencies
```bash
 python -m venv venv
 source venv/bin/activate  # On Windows use `venv\Scripts\activate`
 pip install -r requirements.txt
```
### 🔹 3. Set Up API Keys
Create a `.env` file and add your OpenAI or Anthropic API key:
```plaintext
 OPENAI_API_KEY='your-openai-key'
 ANTHROPIC_API_KEY='your-anthropic-key'
```

---

## 🏗️ Project Structure
```plaintext
📂 ai-meal-planner/
│-- models.py          # Pydantic models for meal planning
│-- app.py             # Streamlit frontend
│-- meal_generator.py  # AI-powered meal generator
│-- .env.example       # Example .env file for API keys
│-- requirements.txt   # Dependencies list
```

---

## 🎨 How It Works?
### 1️⃣ **User Inputs Preferences**
- Dietary restrictions 🍃
- Allergies 🚫
- Disliked ingredients ❌
- Goals (e.g., weight loss, muscle gain) 🎯
- Cuisine preferences 🌎
- Meal complexity 🍽️

### 2️⃣ **LLM Generates a Meal Plan**
A structured prompt is sent to **GPT-4 or Claude 3**, instructing it to generate a JSON-based 7-day meal plan.

### 3️⃣ **Validating & Displaying the Plan**
- JSON is parsed and validated using **Pydantic** ✅
- The structured meal plan is displayed using **Streamlit** 📊

---

## 🖥️ Running the App
```bash
 streamlit run app.py
```
Then open **http://localhost:8501** in your browser.

---

## 🏆 Example Meal Plan Output
```json
{
  "monday": {
    "breakfast": { "meal_name": "Avocado Toast", "recipe": "Toast bread, add mashed avocado, season with salt & pepper." },
    "lunch": { "meal_name": "Grilled Chicken Salad", "recipe": "Grill chicken, mix with greens, cherry tomatoes, and balsamic dressing." },
    "dinner": { "meal_name": "Quinoa Stir-Fry", "recipe": "Cook quinoa, stir-fry with veggies, tofu, and soy sauce." }
  }
}
```

---

## 🌟 Future Enhancements
- 🔥 Add **calorie & macronutrient tracking** 📊
- 📲 Deploy as a **mobile-friendly web app** 🌐
- 🎤 Voice-based meal plan generation 🎙️
- 🛒 **Grocery List Generation** based on meal plan 📋
- 📊 **Nutritional Insights Dashboard** with analytics 📈

---

## 🤝 Contributing
Want to contribute? PRs are welcome! 🎉

---

## 📜 License
MIT License © 2025 Hulk Fitness Meal Planner

---

## 💡 Feedback?
Drop your suggestions in **issues** or reach out on **LinkedIn!** 🚀
