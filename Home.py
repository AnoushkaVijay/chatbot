import streamlit as st

from Utils import create_get_payload, login, create_post_payload, user_sign_up


#IMAGE_ADDRESS = "https://www.researchgate.net/publication/370767314/figure/fig1/AS:11431281211563079@1702429292171/Therapeutic-and-nutritional-management-of-irritable-bowel-syndrome.tif"


if 'login' not in st.session_state:
    st.session_state.login = False

if 'user_id' not in st.session_state:
    st.session_state.user_id = False

# web app
st.title("MemoryLane")
#st.image(IMAGE_ADDRESS, caption = "IBS Nutrition")

log_in, sign_up = st.tabs(["Log In", "Sign Up"])

with sign_up:
    st.header("Please Sign Up")
    with st.form("SignIn Form"):
        username = st.text_input("User Email", placeholder = "Enter your Email Address")
        password = st.text_input("Password", placeholder = "Enter your password", type = "password")
        re_enter_password = st.text_input("Re-Enter Your Password", placeholder = "Enter your password", type = "password")

        submitted = st.form_submit_button("Sign Up")
        if submitted:
            if username and password:
                if password != re_enter_password:
                    st.error("Passwords are not macthing. Please check!")
                    st.stop()
                with st.spinner("Processing......."):
                    payload = create_post_payload(username, password)
                    signin_response = user_sign_up(payload)
                if signin_response["status"] == "failure":
                    st.error(signin_response["errors"][0])
                else:
                    st.session_state.login = False
                    st.success("SignIn Successful! Please log in to the app from LogIn Page!")
            else:
                st.error("Please enter your username or password")

with log_in:
    st.header("Please Log In")

    with st.form("LogIn Form"):
        username = st.text_input("User Email", placeholder = "Enter your Email Address")
        password = st.text_input("Password", placeholder = "Enter your password", type = "password")

        submitted = st.form_submit_button("LogIn")
        if submitted:
            if username and password:
                with st.spinner("Processing......."):
                    payload = create_get_payload(username, password)
                    login_response = login(payload)
                if login_response["status"] == "failure":
                    st.error(login_response["errors"][0], icon = "😄")
                else:
                    st.session_state.login = True
                    st.session_state.user_id = username
                    st.success("LogIn Successful!")
            else:
                st.error("Please enter your username or password")
