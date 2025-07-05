"""
Health & Wellness Planner Agent - Main Entry Point
"""
import streamlit as st
from dotenv import load_dotenv
import random
from datetime import datetime
load_dotenv()
from agent import HealthWellnessAgent
from context import UserSessionContext, RunContextWrapper

# --- New: Habit Tracker Data Structure ---
def get_habits():
    if 'habits' not in st.session_state:
        st.session_state.habits = [
            {'name': 'Drink 8 glasses of water', 'done': False},
            {'name': 'Walk 10,000 steps', 'done': False},
            {'name': 'Meditate 10 minutes', 'done': False},
        ]
    return st.session_state.habits

# --- New: Mood & Energy Log Data Structure ---
def get_mood_logs():
    if 'mood_logs' not in st.session_state:
        st.session_state.mood_logs = []  # Each entry: {'date': ..., 'mood': ..., 'energy': ...}
    return st.session_state.mood_logs

# --- New: Daily Tips ---
DAILY_TIPS = [
    "Drink a glass of water first thing in the morning!",
    "Take a 5-minute stretch break every hour.",
    "Aim for at least 7 hours of sleep tonight.",
    "A short walk after meals helps digestion.",
    "Practice deep breathing to reduce stress.",
    "Celebrate your small wins today!",
    "Try a new healthy recipe this week.",
    "Consistency beats intensity. Small daily actions add up!",
    "Remember to smile and be kind to yourself!"
]

def main():
    """Main entry point for the Health & Wellness Planner Agent"""
    
    # Page config
    st.set_page_config(
        page_title="Health & Wellness Planner",
        page_icon="🏃",
        layout="wide"
    )
    
    # Initialize session state
    if 'agent' not in st.session_state:
        st.session_state.agent = HealthWellnessAgent()
    
    if 'context' not in st.session_state:
        st.session_state.context = RunContextWrapper(UserSessionContext(
            name="",
            uid=12345
        ))
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Title
    st.title("🏃‍♂️ Health & Wellness Planner Agent")
    st.write("Your AI-powered health and wellness assistant!")
    
    # Sidebar
    with st.sidebar:
        st.image("https://media.istockphoto.com/id/1338134319/photo/portrait-of-young-indian-businesswoman-or-school-teacher-pose-indoors.jpg?s=1024x1024&w=is&k=20&c=0yUW1VuW3FizTDgdlHL4zp5Od5X9JCdMJyCXp2WTPx8=", width=130)  # Placeholder avatar
        st.header("Your Profile")
        name = st.text_input("Name", value=st.session_state.context.get_context().name)
        if name != st.session_state.context.get_context().name:
            st.session_state.context.update_context(name=name)
        
        # Show current goal
        goal = st.session_state.context.get_context().goal
        if goal:
            if isinstance(goal, dict):
                st.write(f"**Current Goal:** {goal.get('original_text', 'Not set')}")
            else:
                st.write(f"**Current Goal:** {goal}")
        
        # Progress bar for weekly workouts (placeholder)
        st.write("**Weekly Workouts**")
        st.progress(0.4, text="2/5 workouts")
        
        # Random daily tip
        st.markdown(f"> 💡 **Tip:** {random.choice(DAILY_TIPS)}")
        
        # Quick actions
        st.header("Quick Actions")
        if st.button("🎯 Set Goal"):
            st.session_state.messages.append({"role": "user", "content": "I want to set a fitness goal"})
            st.rerun()
        
        if st.button("🍽️ Meal Plan"):
            st.session_state.messages.append({"role": "user", "content": "I need a meal plan"})
            st.rerun()
        
        if st.button("💪 Workout Plan"):
            st.session_state.messages.append({"role": "user", "content": "I need a workout plan"})
            st.rerun()
    
    # Main Tabs
    tabs = st.tabs(["💬 Chat", "📊 Progress", "✅ Habits", "📚 Resources"])
    
    # Chat Tab
    with tabs[0]:
        st.header("💬 Chat with Your Assistant")
        
        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # User input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.agent.process_message(prompt, st.session_state.context)
                        
                        if response['response_type'] == 'error':
                            st.error(f"Error: {response['content']['error']}")
                        else:
                            # Display response based on type
                            content = response['content']
                            
                            if isinstance(content, dict):
                                if 'message' in content:
                                    st.info(content['message'])
                                
                                # Display structured content
                                if 'daily_plans' in content:
                                    st.subheader("🍽️ Your 7-Day Meal Plan")
                                    for day_plan in content['daily_plans']:
                                        with st.expander(f"{day_plan['day']} - {day_plan.get('calories', 'N/A')} calories"):
                                            meals = day_plan['meals']
                                            st.write(f"**Breakfast:** {meals['breakfast']}")
                                            st.write(f"**Lunch:** {meals['lunch']}")
                                            st.write(f"**Dinner:** {meals['dinner']}")
                                            st.write(f"**Snack:** {meals['snack']}")
                                
                                elif 'weekly_plan' in content:
                                    st.subheader("💪 Your Workout Plan")
                                    for day_plan in content['weekly_plan']:
                                        with st.expander(f"{day_plan['day']} - {day_plan['focus']}"):
                                            st.write(f"**Exercises:** {', '.join(day_plan['exercises'])}")
                                            st.write(f"**Duration:** {day_plan.get('duration', '30 minutes')}")
                                            if 'notes' in day_plan:
                                                st.write(f"**Notes:** {day_plan['notes']}")
                                
                                elif 'recommendations' in content:
                                    st.subheader("📋 Recommendations")
                                    for rec in content['recommendations']:
                                        if isinstance(rec, dict):
                                            priority = rec.get('priority', 'medium')
                                            color = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '🟡')
                                            st.write(f"{color} **{rec.get('category', 'General').title()}:** {rec.get('recommendation', '')}")
                                        else:
                                            st.write(f"• {rec}")
                                
                                elif 'capabilities' in content:
                                    st.write("I can help you with:")
                                    for cap in content['capabilities']:
                                        st.write(f"• {cap}")
                            
                            else:
                                st.write(content)
                            
                            # Add to messages
                            st.session_state.messages.append({"role": "assistant", "content": str(content)})
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    # Progress Tab (placeholder for future chart integration)
    with tabs[1]:
        st.header("📊 Progress Visualization (Coming Soon)")
        st.info("Charts and analytics for your progress will appear here.")

    # Habits Tab
    with tabs[2]:
        st.header("✅ Habit Tracker")
        habits = get_habits()
        all_done = all(h['done'] for h in habits) if habits else False
        for i, habit in enumerate(habits):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(habit['name'])
            with col2:
                checked = st.checkbox("Done", value=habit['done'], key=f"habit_{i}")
                habits[i]['done'] = checked
        new_habit = st.text_input("Add a new habit", key="new_habit")
        if st.button("Add Habit") and new_habit:
            habits.append({'name': new_habit, 'done': False})
            st.session_state.new_habit = ""
            st.experimental_rerun()
        # Mood & Energy Logging
        st.subheader("Log Your Mood & Energy")
        with st.form("mood_form"):
            mood = st.selectbox("Mood", ["😀 Happy", "🙂 Good", "😐 Neutral", "🙁 Low", "😞 Sad"])
            energy = st.slider("Energy Level", 1, 10, 5)
            submitted = st.form_submit_button("Log Mood & Energy")
            if submitted:
                mood_logs = get_mood_logs()
                mood_logs.append({
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'mood': mood,
                    'energy': energy
                })
                st.success("Mood & energy logged!")
        # Celebratory feedback
        if all_done and habits:
            st.balloons()
            st.success("Congratulations! You completed all your habits today!")

    # Resources Tab
    with tabs[3]:
        st.header("📚 Resource Library")
        st.write("- [CDC Healthy Living](https://www.cdc.gov/healthyweight/index.html)")
        st.write("- [WHO Physical Activity](https://www.who.int/news-room/fact-sheets/detail/physical-activity)")
        st.write("- [Harvard Nutrition Source](https://www.hsph.harvard.edu/nutritionsource/)")

if __name__ == "__main__":
    main()