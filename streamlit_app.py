import streamlit as st
from decouple import config
from PIL import Image
import json
import os

# Function to handle successful charge
def handle_charge_success(event):
    charge = event['data']['object']
    # Extract relevant payment information and update your app accordingly
    # For example, you can store the payment status in your database or display a success message to the user
    st.write("Payment successful! Thank you for your purchase.")
    # Initiate session
    st.session_state['logged_in'] = True

# Your existing Streamlit app code
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

# Check if Stripe event received
stripe_event_json = os.getenv("STRIPE_EVENT")
if stripe_event_json:
    try:
        st.write("Stripe Event Payload:", stripe_event_json)  # Print the entire Stripe event payload
        event = json.loads(stripe_event_json)
        handle_charge_success(event)
    except Exception as e:
        st.error(f"Error handling Stripe event: {e}")

if 'logged_in' in st.session_state.keys() and not st.session_state['logged_in']:
    if submitted and password == config('SECRET_PASSWORD'):
        st.session_state['logged_in'] = True
        st.text('Successfully Logged In!')
    else:
        st.text('Incorrect login credentials.')
        st.session_state['logged_in'] = False

if 'logged_in' in st.session_state.keys() and st.session_state['logged_in']:
    st.markdown('## Ask Me Anything')
    question = st.text_input('Ask your question')
    if question != '':
        st.write('I drink and I know things.')

