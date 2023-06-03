import streamlit as st

import llm_explorer.interfaces.frontend as it
from llm_explorer.agents import pandas_agent

st.text("LLM Explorer.")
st.warning(
    "It uses Langchain Agent for Pandas with OpenAI GPT3.5 API to generate a step by step explanation of the code used to generate a time series prediction"
)

it.display_sidebar()
pandas_agent()
