import streamlit as st

# Function to suggest meals
def suggest_meal(diet_type, cheat_day):
    if cheat_day:
        return f"Here's a cheat meal plan for your {diet_type} diet."
    else:
        return f"Here's a regular meal plan for your {diet_type} diet."

# Function to suggest exercises
def suggest_exercise(workout_days, workout_duration):
    try:
        workout_days = int(workout_days)
        workout_duration = int(workout_duration)
    except ValueError:
        return "Please enter valid numbers for workout days and duration."

    if workout_days >= 4:
        return "You should focus on high-intensity workouts like HIIT or strength training."
    elif workout_days >= 2:
        return "Moderate exercise is best for you. A mix of cardio and strength training."
    else:
        return "Light exercises such as walking or stretching would be suitable."

# Streamlit app title
st.title("Fitness and Diet Chatbot")

# Initialize session state variables if not already set
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "stage" not in st.session_state:
    st.session_state.stage = "name"

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "reset_input" not in st.session_state:
    st.session_state.reset_input = False

# Function to process chatbot conversation
def chat(message):
    message = message.strip()
    st.session_state.conversation.append(f"*User :* {message}")

    if st.session_state.stage == "name":
        st.session_state.user_data["name"] = message.title()
        st.session_state.stage = "workout"
        return "Do you work out? (Yes/No)"

    elif st.session_state.stage == "workout":
        if message.lower() in ["yes", "y"]:
            st.session_state.user_data["workout"] = True
            st.session_state.stage = "workout_duration"
            return "How long do you work out for (in minutes)?"
        else:
            st.session_state.user_data["workout"] = False
            st.session_state.stage = "diet_type"
            return "What is your diet type? (Vegetarian/Non-Vegetarian/Vegan)?"

    elif st.session_state.stage == "workout_duration":
        if message.isdigit() and int(message) > 0:
            st.session_state.user_data["workout_duration"] = message
            st.session_state.stage = "workout_days"
            return "How many days a week do you work out?"
        else:
            return "Please enter a valid number for workout duration."

    elif st.session_state.stage == "workout_days":
        if message.isdigit() and int(message) > 0:
            st.session_state.user_data["workout_days"] = message
            st.session_state.stage = "cheat_day"
            return "Do you have cheat days? (Yes/No)"
        else:
            return "Please enter a valid number for workout days."

    elif st.session_state.stage == "cheat_day":
        st.session_state.user_data["cheat_day"] = message.lower() in ["yes", "y"]
        st.session_state.stage = "diet_type"
        return "What is your diet type? (Vegetarian/Non-Vegetarian/Vegan)?"

    elif st.session_state.stage == "diet_type":
        if message.capitalize() in ["Vegetarian", "Non-Vegetarian", "Vegan"]:
            st.session_state.user_data["diet_type"] = message.capitalize()
            meal_suggestion = suggest_meal(st.session_state.user_data["diet_type"], st.session_state.user_data["cheat_day"])
            exercise_suggestion = suggest_exercise(st.session_state.user_data.get("workout_days", 0), st.session_state.user_data.get("workout_duration", 0))
            
            st.session_state.stage = "done"
            return f"*Here are your personalized recommendations:\n\n🍽 **Meal Plan:* {meal_suggestion}\n🏋️ *Workout Plan:* {exercise_suggestion}"
        else:
            return "Please enter a valid diet type (Vegetarian/Non-Vegetarian/Vegan)."

# Input field for user response
user_input = st.text_input("Your name:", key="user_input", placeholder="Type your message here...")

# Process chatbot response when user submits input
if st.session_state.reset_input:
    user_input = ""
    st.session_state.reset_input = False

if user_input:
    bot_reply = chat(user_input)
    st.session_state.conversation.append(f"*Bot:* {bot_reply}")
    st.session_state.reset_input = True  # Set flag to clear input field

# Display conversation history
st.text_area("Conversation so far:", value="\n".join(st.session_state.conversation), height=400, disabled=True)