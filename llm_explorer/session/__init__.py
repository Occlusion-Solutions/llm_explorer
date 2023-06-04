# Streamlit Session parameters linked to pydantic datamodels
import streamlit as st
from llm_explorer.datamodels.interfacing import SessionState


class Session:
    def __init__(self, session_state: SessionState):
        self.session_state = session_state

    @property
    def session_state(self):
        return self._session_state

    @property
    def databricks(self):
        return self._session_state.databricks

    @property
    def mlflow(self):
        return self._session_state.mlflow

    @property
    def snowpark(self):
        return self._session_state.snowpark


def streamlit_session():
    return Session().session_state


# Databricks Session


# MLFlow Session


# Snowpark Session
