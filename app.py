# filename: app.py

import streamlit as st
import chat

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'initial'
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'initial_thoughts' not in st.session_state:
    st.session_state.initial_thoughts = ''
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# Layout
st.title("Newsletter Writer Assistant")

api_key = st.text_input(
    "Enter your LLM API Key (required):",
    type="password",
    help="We need your API key to generate personalized questions. It will not be stored."
)

# Step 1: Collect Initial Thoughts
if st.session_state.step == 'initial':
    st.subheader("Step 1: Enter your initial ideas")
    initial_input = st.text_area("Your initial thoughts", value=st.session_state.initial_thoughts, height=200)
    
    if st.button("Submit Initial Thoughts"):
        if initial_input.strip() != "":
            st.session_state.initial_thoughts = initial_input
            st.session_state.questions = chat.get_questions(initial_input,api_key)
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.step = 'questions'
            # No need for st.experimental_rerun()

# Step 2: Ask Sequential Questions
elif st.session_state.step == 'questions':
    st.subheader(f"Step 2: Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}")
    st.write(st.session_state.questions[st.session_state.current_question])
    
    answer = st.text_area("Your answer", key=f"answer_{st.session_state.current_question}")

    if st.button("Submit Answer"):
        if answer.strip() != "":
            st.session_state.answers.append(answer)
            st.session_state.current_question += 1
            if st.session_state.current_question >= len(st.session_state.questions):
                st.session_state.step = 'generate'
            # No need for st.experimental_rerun()

# Step 3: Generate Newsletter
elif st.session_state.step == 'generate':
    st.subheader("Step 3: Generate Newsletter")
    
    if st.button("Generate Newsletter"):
        newsletter = "**Newsletter Draft**\n\n"
        newsletter += f"**Initial Thoughts:**\n{st.session_state.initial_thoughts}\n\n"
        for q, a in zip(st.session_state.questions, st.session_state.answers):
            newsletter += f"**{q}**\n{a}\n\n"
        
        st.session_state.generated_newsletter = newsletter
        st.session_state.step = 'display'
        # No need for st.experimental_rerun()

# Step 4: Display Final Draft
elif st.session_state.step == 'display':
    st.subheader("Your Newsletter Draft")
    st.markdown(st.session_state.generated_newsletter)

    st.download_button(
        label="Download Newsletter",
        data=st.session_state.generated_newsletter,
        file_name='newsletter_draft.txt',
        mime='text/plain'
    )
    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # No need for st.experimental_rerun()
