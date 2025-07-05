# Health & Wellness Planner Agent

A simple AI-powered health and wellness assistant built with Python, Streamlit, and OpenAI SDK (using Gemini API).

## Features

- 🎯 Goal analysis and planning
- 🍽️ Personalized meal plans
- 💪 Workout recommendations
- 📊 Progress tracking
- 📅 Check-in scheduling
- 🤝 Specialist agent handoffs
- 🔒 Input/output guardrails
- 🔄 Real-time streaming (basic)
- 📝 Lifecycle hooks for logging

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Add your Gemini API key to .env
   ```

3. **Run the app:**
   ```bash
   streamlit run main.py
   ```

## Project Structure

```
health_wellness_agent/
├── main.py                    # Streamlit frontend
├── agent.py                   # Main agent
├── context.py                 # Context management
├── guardrails.py             # Input/output validation
├── hooks.py                  # Lifecycle hooks
├── tools/                    # Tool implementations
│   ├── goal_analyzer.py
│   ├── meal_planner.py
│   ├── workout_recommender.py
│   ├── scheduler.py
│   └── tracker.py
├── agents/                   # Specialized agents
│   ├── escalation_agent.py
│   ├── nutrition_expert_agent.py
│   └── injury_support_agent.py
└── utils/                    # Utilities
    └── streaming.py
```

## How It Works

1. **Chat Interface:** Simple Streamlit chat interface
2. **Intent Detection:** Basic keyword matching to determine user intent
3. **Tool Routing:** Routes to appropriate tool based on intent
4. **Handoff Logic:** Transfers to specialist agents when needed
5. **Context Management:** Maintains user session state
6. **Guardrails:** Validates inputs and outputs
7. **Hooks:** Logs activities and tracks metrics

## Example Usage

- "I want to lose 5kg in 2 months" → Goal Analyzer Tool
- "I'm vegetarian and need a meal plan" → Meal Planner Tool
- "I have knee pain" → Injury Support Agent
- "I'm diabetic" → Nutrition Expert Agent
- "I want to talk to a human coach" → Escalation Agent

## Configuration

The app uses OpenAI SDK configured for Gemini API:

```python
# In .env file
OPENAI_API_KEY=your_gemini_api_key
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/
OPENAI_MODEL=gemini-pro
```

## Simple Architecture

This is a beginner-friendly implementation with:
- Basic intent detection using keyword matching
- Simple tool routing
- Straightforward handoff logic
- Basic context management
- Simple guardrails
- Basic logging hooks

Perfect for learning how AI agents work!