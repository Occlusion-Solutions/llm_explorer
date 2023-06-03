# import pyautogui
from typing import Union

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from explorer.databases.adbddl import ADBDDL
from explorer.indexes.vectorstore import faiss_metadata_index_loader
from explorer.ui import UI

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
    elif choice == "explorer/pages/pandas_agent":
        st.write("Run pages/pandas_agent")

    # option_names = ["a", "b", "c"]
    # output_container = st.empty()
    # next = st.button("Next/save")
    # if next:
    #     if st.session_state["radio_option"] == 'a':
    #         st.session_state.radio_option = 'b'
    #     elif st.session_state["radio_option"] == 'b':
    #         st.session_state.radio_option = 'c'
    #     else:
    #         st.session_state.radio_option = 'a'

    # option = st.sidebar.radio("Pick an option", option_names , key="radio_option")
    # st.session_state

    # if option == 'a':
    #     output_container.write("You picked 'a' :smile:")
    # elif option == 'b':
    #     output_container.write("You picked 'b' :heart:")
    # else:
    #     output_container.write("You picked 'c' :rocket:")

    # st.selectbox("Select an Interaction Mode", options=['explorer','pages/pandas_agent'])
    # import pyautogui
    # import streamlit as l

    # # create a button in the side bar that will move to the next page/radio button choice
    # next = st.sidebar.button('Next on list')
    # ## will use this list and next button to increment page, MUST BE in the SAME order
    # # as the list passed to the radio button
    # new_choice = ['Home', 'Resources', 'Gallery', 'Vision', 'About']
    # choice = st.sidebar.radio("go to", ('Home', 'Resources', 'Gallery', 'Vision', 'About'))
    # # Take care of scrolling
    # if next:
    #     pyautogui.press("tab")
    #     pyautogui.press("down")
    # else:
    #     # create your radio button with the index that we loaded
    #     # finally get to whats on each page
    #     if choice == 'Home':
    #         st.write("this is home")
    #     elif choice == 'Resources':
    #         st.write('here is a resources page')
    #     elif choice == 'Gallery':
    #         st.write('A Gallery of some sort')
    #     elif choice == 'Vision':
    #         st.write('The Vision')
    #     elif choice == 'About':
    #         st.write('About page')
