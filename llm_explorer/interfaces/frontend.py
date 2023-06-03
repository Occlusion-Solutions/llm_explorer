# import pyautogui
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from llm_explorer.databases.adbddl import ADBDDL
from llm_explorer.indexes.vectorstore import faiss_metadata_index_loader
from llm_explorer.ui import UI

adb_ddl = ADBDDL()


def display_header() -> None:
    # st.image("img/logo.jpg")
    st.title("LLM Explorer")
    # Create a description based on the smart gpt and queried defined here
    st.caption(
        "Self service Tool for Interaction, jobs creation, interaction with Engines and Lakehouse Analysis"
    )
    styles_content = UI.styles()
    st.write(styles_content, unsafe_allow_html=True)


def display_widgets(default_path):
    file = st.file_uploader("Upload your file here.")
    if not (file):
        st.error("Upload a time series file .csv with columns: ts_id, ds, y")
    return file or default_path


def retrieve_content_from_file(file: UploadedFile) -> str:
    return file.getvalue().decode("utf8")


def display_sidebar() -> None:
    sidebar_content = UI.sidebar()
    st.sidebar.markdown(sidebar_content)

    # Create a sidebar with a dropdown menu
    selected_table = st.sidebar.selectbox(
        "Select a table:", options=list(adb_ddl.ddl_dict.keys())
    )
    st.sidebar.markdown(f"### DDL for {selected_table} table")
    st.sidebar.code(adb_ddl.ddl_dict[selected_table], language="sql")

    # create a button in the side bar that will move to the next page/radio button choice
    next = st.sidebar.button("Next on list")
    ## will use this list and next button to increment page, MUST BE in the SAME order
    # as the list passed to the radio button
    new_choice = [
        "Explorer",
        "Update Vector Store",
    ]
    choice = st.sidebar.radio(
        "Run",
        (
            "Explorer",
            "Update Vector Store",
        ),
    )
    # Take care of scrolling
    if next:
        ...
        # pyautogui.press("tab")
        # pyautogui.press("down")
    elif choice == "Explorer":
        st.write("Explorer")
    elif choice == "Update Vector Store":
        faiss_metadata_index_loader()
        st.write("Run Update Vector Store")
    elif choice == "llm_explorer/pages/pandas_agent":
        st.write("Run pages/pandas_agent")
