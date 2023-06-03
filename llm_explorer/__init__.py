# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "LLM Explorer"
PAGE_ICON: str = "🤖🎯"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
LANG_ES: str = "Es"

import streamlit as st

from .ui import about

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "mailto:carlos@occlusion.solutions",
        "About": about(),
    },
)

from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from .chains import ExplorerConversationChain
from .chat import chat_loop
from .interfaces import frontend as it
from .ui.lang import en, es


def auth():
    import streamlit_authenticator as stauth
    import yaml
    from yaml.loader import SafeLoader

    with open("llm_explorer/auth/access.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

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


load_dotenv(find_dotenv())
chain = ExplorerConversationChain()

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = "llm_explorer/ui/styles/.css"
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"


# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# selected_lang = option_menu(
#     menu_title=None,
#     options=[LANG_EN, LANG_RU, LANG_ES],
#     icons=["globe2", "translate"],
#     menu_icon="cast",
#     default_index=0,
#     orientation="horizontal",
#     styles=HEADER_STYLES
# )

# # Storing The Context
# if "locale" not in st.session_state:
#     st.session_state.locale = en
# if "generated" not in st.session_state:
#     st.session_state.generated = []
# if "past" not in st.session_state:
#     st.session_state.past = []
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "user_text" not in st.session_state:
#     st.session_state.user_text = ""
# if "input_kind" not in st.session_state:
#     st.session_state.input_kind = st.session_state.locale.input_kind_1
# if "seed" not in st.session_state:
#     st.session_state.seed = 420# noqa: S311
# if "costs" not in st.session_state:
#     st.session_state.costs = []
# if "total_tokens" not in st.session_state:
#     st.session_state.total_tokens = []


def main() -> None:
    it.display_header()
    it.display_sidebar()
    if auth():
        chat_loop(chain)
    else:
        st.write("You are not authorized to access this page.")


if __name__ == "__main__":
    main()
