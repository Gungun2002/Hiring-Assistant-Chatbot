from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize Groq model
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY is not set. Please check your .env file.")
    st.stop()

model = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key)  # Corrected model name

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to interact with Groq API
def chat_with_groq(prompt):
    try:
        response = model.invoke(prompt)  # Use invoke method from LangChain
        return response  # Directly return the response
    except Exception as e:
        st.error(f"Error: {e}")  # Show error in UI
        return "I'm sorry, I couldn't process that request."

# Streamlit UI
st.title("TalentScout Hiring Assistant 🤖")
st.write("Hello! I’m here to assist with your hiring process.")

# Collect candidate information
full_name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
experience = st.number_input("Years of Experience", min_value=0, max_value=50)
position = st.text_input("Desired Position")
location = st.text_input("Current Location")
tech_stack = st.text_area("Tech Stack (e.g., Python, Django, SQL)")

# Generate Technical Questions
if st.button("Generate Technical Questions"):
    if not tech_stack:
        st.error("Please enter your tech stack.")
    else:
        user_prompt = f"Generate 3-5 technical interview questions for a candidate proficient in {tech_stack}."
        st.session_state.messages.append(("user", user_prompt))
        
        questions = chat_with_groq(user_prompt)  # Get response from Groq API
        
        st.session_state.messages.append(("bot", questions))
        st.write(questions)

# Display Chat History
st.subheader("Chat History")
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)

# End conversation
if st.button("End Conversation"):
    st.session_state.messages = []
    st.success("Thank you! We’ll get back to you soon.")
