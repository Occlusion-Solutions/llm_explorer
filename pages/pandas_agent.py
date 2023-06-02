import streamlit as st

import explorer.interfaces.frontend as it
from explorer.agents import pandas_agent

st.text("LLM Explorer.")
st.warning("It uses Langchain Agent for Pandas with OpenAI GPT3.5 API to generate a step by step explanation of the code used to generate a time series prediction")

it.display_sidebar()
pandas_agent()
