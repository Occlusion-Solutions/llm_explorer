import streamlit as st
from langchain.llms import OpenAI


def set_llm(**kwargs):
    if "llm" in st.session_state:
        return st.session_state.llm
    else:
        st.session_state.llm = OpenAI(
                    temperature=st.session_state.llm_temperature.get("temperature", 0),
                    openai_api_key=st.secrets.connections.openai.api_key,
                    model_name="gpt-3.5-turbo",
                    max_tokens=st.session_state.llm_max_tokens.get("max_tokens", -1),  # Max number of tokens to generate
                    # top_p=kwargs.get(
                    #     "top_p", 1
                    # ),  # Total probability mass of tokens to consider at each step
                    # frequency_penalty=kwargs.get(
                    #     "frequency_penalty", 0
                    # ),  # Penalizes repeated tokens according to frequency
                    # presence_penalty=kwargs.get(
                    #     "presence_penalty", 0
                    # ),  # Penalizes repeated tokens.
                    # n=kwargs.get("n", 1),  # How many completions to generate for each prompt.
                    # best_of=kwargs.get(
                    #     "best_of", 1
                    # ),  # Generates best_of completions server-side and returns the "best".
                )