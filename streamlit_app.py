import streamlit as st
from decouple import config
from PIL import Image
import openai
import time

# Configure OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]
assistant_id = "your-assistant-id"  # Replace "your-assistant-id" with your OpenAI assistant ID

st.set_page_config(page_icon='🗡', page_title='Streamlit Paywall Example')

st.markdown('## Chat with Tyrion Lannister ⚔️')
col1, col2 = st.columns((2,1))
with col1:
    st.markdown(
        f"""
        Chat with Tyrion Lannister to advise you on:
        - Office Politics
        - War Strategy
        - The Targaryens


        #### [Sign Up Now 🤘🏻]({config('STRIPE_CHECKOUT_LINK')})
        """
    )
with col2:
    image = Image.open('./assets/DALL·E 2023-01-08 17.53.04 - futuristic knight robot on a horse in cyberpunk theme.png')
    st.image(image)


st.markdown('### Already have an Account? Login Below👇🏻')
with st.form("login_form"):
    st.write("Login")
    email = st.text_input('Enter Your Email')
    password = st.text_input('Enter Your Password')
    submitted = st.form_submit_button("Login")

if submitted:
    if password == config('SECRET_PASSWORD'):
        st.session_state['logged_in'] = True
        st.text('Succesfully Logged In!')
    else:
        st.text('Incorrect, login credentials.')
        st.session_state['logged_in'] = False

if 'logged_in' in st.session_state.keys():
    if st.session_state['logged_in']:
        st.session_state.start_chat = True
        thread = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "assistant", "content": "Hi, Do you want to start a new career or business? Or maybe improvement? I can help you in this task."}
            ],
            max_tokens=150,
            temperature=0.7
        )

        st.session_state.thread_id = thread.id
        messages = thread.messages

        for message in messages:
            if message.role == "user":
                st.write(f"User: {message.content}")
            elif message.role == "assistant":
                st.write(f"Assistant: {message.content}")
