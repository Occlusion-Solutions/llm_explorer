# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "LLM Explorer"
PAGE_ICON: str = "🤖🎯"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
LANG_ES: str = "Es"

import streamlit as st

from llm_explorer.ui import about

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

from llm_explorer.chains import ExplorerConversationChain
from llm_explorer.chat import chat_loop
from llm_explorer.interfaces import frontend as it
from llm_explorer.ui.lang import en, es, Locale
from llm_explorer.ui.styles import load_css
from llm_explorer.login import auth



load_dotenv(find_dotenv())
chain = ExplorerConversationChain()
load_css()


def main() -> None:
    it.display_header()
    it.display_sidebar()
    if auth():
        chat_loop(chain)
    else:
        st.write("You are not authorized to access this page.")

if __name__ == "__main__":
    main()
