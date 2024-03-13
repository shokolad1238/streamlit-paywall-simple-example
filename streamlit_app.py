import streamlit as st
import json

# Function to handle charge succeeded event
def handle_charge_succeeded(event):
    charge_id = event['data']['object']['id']
    amount = event['data']['object']['amount']
    currency = event['data']['object']['currency']
    # Add your logic to update the app based on the charge details
    st.write(f"Charge ID: {charge_id}")
    st.write(f"Amount: {amount / 100} {currency}")  # Assuming amount is in cents, convert to dollars
    st.write("Payment successful! Thank you for your purchase.")

# Listen for incoming webhook requests
if st.request.method == 'POST':
    payload = st.request.body.decode('utf-8')
    event = json.loads(payload)
    
    if event['type'] == 'charge.succeeded':
        handle_charge_succeeded(event)
    else:
        st.write(f"Received unsupported event type: {event['type']}")

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

