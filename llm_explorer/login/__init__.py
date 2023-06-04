import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st


def get_auth_file(file_path: str = "llm_explorer/auth/access.yaml"):
    with open(file_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


def get_login_session_state(config) -> str:
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )

    name, authentication_status, username = authenticator.login("Login", "main")
        
    # if st.session_state["authentication_status"]:
    #     authenticator.logout('Logout', 'main')
    #     st.write(f'Welcome *{st.session_state["name"]}*')
    #     st.title('LLM Explorer')
    # elif st.session_state["authentication_status"] == False:
    #     st.error('Username/password is incorrect')
    # elif st.session_state["authentication_status"] == None:
    #     st.warning('Please enter your username and password')

    if authentication_status:
        authenticator.logout("Logout", "main")
        if username in config["preauthorized"]["users"]:
            st.write(f"Welcome *{username}*")
            return True
        else:
            st.error("Username/password is incorrect")
            return False
    elif authentication_status == False:
        st.error("Username/password is incorrect")
        return False
    elif authentication_status is None:
        st.warning("Please enter your username and password")

    return authentication_status

def auth():
    config = get_auth_file()
    authentication_status = get_login_session_state(config)
    return authentication_status