import contextlib

import pandas as pd
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from langchain import ConversationChain, LLMChain, OpenAI
from langchain.agents import (
    AgentExecutor,
    AgentType,
    Tool,
    ZeroShotAgent,
    create_pandas_dataframe_agent,
    initialize_agent,
    load_tools,
)
from langchain.agents.load_tools import get_all_tool_names

import llm_explorer.interfaces.frontend as it
from llm_explorer.templates.agents import agents_templates
from llm_explorer.templates.prompt import prompt_templates

load_dotenv(find_dotenv())


class TSELLMAgent:
    def __init__(self, agent_id: str = "smart_gpt"):
        self.agent_templates = agents_templates()
        self.agent_id = agent_id

    def execute(self, query, df):
        with contextlib.suppress(Exception):
            # Try to get the ts_id from the dataframe
            ts_id = df["ts_id"].unique()[0]
            df.drop(columns=["ts_id"], inplace=True)
            cols = df.columns.tolist()
            return self.run_pandas_agent(
                query.format({"ts_id": ts_id, "cols": cols}), df.tail(10)
            )
        return self.run_pandas_agent(query, df.tail(10))

    def run_pandas_agent(
        self,
        query: str,
        df,
    ) -> str:
        llm = OpenAI()
        get_all_tool_names()
        tools = load_tools(
            ["llm-math", "open-meteo-api", "requests_all", "terminal", "python_repl"],
            llm=llm,
        )

        agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            tools=tools,
            # verbose=True,
            max_iterations=15,
            early_stopping_method="force",
        )
        return agent.run(self.agent_templates[self.agent_id].format(prompt=query))

    def run_agent_query(self, uploaded_file, query):
        st.write("Executing LLM Agent...")
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.style.highlight_max(axis=0))
        except Exception as e:
            print(e)
            df = None
        with st.spinner(text="Executing LLM Agent..."):
            agent_results = self.execute(query=query, df=df)
            st.success("Completed inferece!")
            st.markdown(f"**Explanation:** {agent_results}")


def pandas_agent():
    uploaded_file = it.display_widgets(
        "llm_explorer/indexes/samples/telemetry_sample_forecast.csv"
    )
    sample_df = pd.read_csv(uploaded_file)
    st.write("Sample of loaded table:")
    st.table(sample_df.head(3))
    # Create the Streamlit dropdown
    option = st.selectbox(
        "Sample Prompt",
        list(prompt_templates().keys()),
    )
    query = ""
    if not (query):
        st.error("Edit Inserted Prompt")
    query = st.text_area(
        label=f"{option}:",
        value=prompt_templates()[option],
        height=200,
    )

    agent = TSELLMAgent()
    if st.button("Run"):
        agent.run_agent_query(uploaded_file=uploaded_file, query=query)


from typing import Type

import streamlit as st
from transformers import HfAgent, OpenAiAgent

# import soundfile as sf

# def play_audio(audio):
#     sf.write("speech_converted.wav", audio.numpy(), samplerate=16000)


class TransformerAgents:
    @staticmethod
    def load_starcoder_agent(
        api_path: str = "https://api-inference.huggingface.co/models/bigcode/starcoder",
    ):
        return HfAgent(api_path)

    @staticmethod
    def load_openassistant_agent(
        api_path: str = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
    ):
        return HfAgent(api_path)

    @staticmethod
    def load_openai_agent(
        model: str = "gpt-3.5-turbo",
        api_key: str = st.secrets.connections.openai.api_key,
    ):
        return OpenAiAgent(model=model, api_key=api_key)


class HFTAgent:
    def __init__(self, agent_name: str = "openai", **kwargs):
        def get_agent_strategy(agent_name):
            agent_strategies = {
                "openai": TransformerAgents.load_openai_agent,
                "starcoder": TransformerAgents.load_starcoder_agent,
                "openassistant": TransformerAgents.load_openassistant_agent,
            }
            return agent_strategies[agent_name]()

        self.kwargs = kwargs
        self.agent = get_agent_strategy(agent_name)

    def run(self, query):
        return self.agent.run(query, **self.kwargs)

    def chat(self, query):
        return self.agent.chat(query, **self.kwargs)

    def clean_chat(self):
        self.agent.prepare_for_new_chat()


from typing import List

import pandas as pd
import streamlit as st
from langchain.agents import AgentExecutor, create_sql_agent, load_tools
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.agents.load_tools import get_all_tool_names
from langchain.base_language import BaseLanguageModel
from langchain.llms.openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.sql_database import SQLDatabase
from langchain.tools import BaseTool
from langchain.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QueryCheckerTool,
    QuerySQLDataBaseTool,
)
from pydantic import Field
from sqlalchemy import *
from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *

# from pip._internal import main as pipmain
# pipmain(['install', 'sqlalchemy-databricks'])


class LLMExplorerToolkit(BaseToolkit):
    """
    Toolkit for LLM Explorer, lakehouse interaction.

    This is a subclass of the BaseToolkit class from the langchain.agents.agent_toolkits.base module.
    It defines a set of tools that can be used to interact with a SQL database.
    """

    db: SQLDatabase = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)

    @property
    def dialect(self) -> str:
        """
        Return string representation of dialect to use.
        """
        return self.db.dialect

    class Config:
        """
        Configuration for this Pydantic object.
        """

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """
        Get the tools in the toolkit.
        """
        return [
            QuerySQLDataBaseTool(db=self.db),
            InfoSQLDatabaseTool(db=self.db),
            ListSQLDatabaseTool(db=self.db),
            QueryCheckerTool(db=self.db, llm=self.llm),
        ] + self.define_explorer_tools()

    def define_explorer_tools(self):
        """
        Define the LLM Explorer tools to be used in the toolkit.
        """
        get_all_tool_names()
        return load_tools(
            ["llm-math", "open-meteo-api", "requests_all", "terminal", "python_repl"],
            llm=self.llm,
        )


class ExplorerAgent:
    """
    An agent designed to interact with a SQL database and return answers to user input questions.

    Attributes:
    -----------
    _server_hostname: str
        The hostname of the Databricks server.
    _http_path: str
        The path to access the Databricks server over HTTP.
    _access_token: str
        The access token used to authenticate the agent with the Databricks server.
    _port: int
        The port number to connect to the Databricks server.
    _database: str
        The name of the database to connect to.
    _engine: sqlalchemy.engine.base.Engine
        The database engine used to connect to the Databricks server.
    _llm: openai_sql.OpenAI
        The OpenAI language model used to generate SQL queries.
    _database_connection: openai_sql.SQLDatabase
        The connection to the SQL database.
    _toolkit: openai_sql.LLMExplorerToolkit
        The toolkit used to explore the SQL database.
    memory: openai_sql.ConversationBufferMemory
        The conversation memory buffer used to store previous user inputs and outputs.
    SQL_PREFIX: str
        The prefix added to the SQL query generated by the agent.
    SQL_SUFFIX: str
        The suffix added to the SQL query generated by the agent.
    PREFIX: str
        The prefix added to the input question asked by the agent.
    FORMAT_INSTRUCTIONS: str
        The format instructions for the user's response.
    agent_executor: openai_sql.SQLAgent
        The SQL agent that executes the SQL query generated by the agent.

    Methods:
    --------
    __init__(self, **kwargs):
        Initializes the ExplorerAgent class by setting its attributes and creating the necessary connections.
    """

    def __init__(self, **kwargs):
        """
        Initializes the ExplorerAgent class by setting its attributes and creating the necessary connections.

        Parameters:
        -----------
        **kwargs: dict
            A dictionary of keyword arguments to set optional attributes.
        """
        # Set attributes from Streamlit secrets and input parameters
        self._server_hostname = st.secrets.connections.databricks.server_hostname
        self._http_path = st.secrets.connections.databricks.http_path
        self._access_token = st.secrets.connections.databricks.access_token
        self._port = 443
        self._database = kwargs.get("database", "default")

        # Create the database engine and OpenAI language model
        self._engine = create_engine(
            f"databricks+connector://token:{self._access_token}@{self._server_hostname}:{self._port}/{self._database}",
            connect_args={
                "http_path": self._http_path,
            },
        )
        self._llm = OpenAI(temperature=0, verbose=True)
        self._database_connection = SQLDatabase(engine=self._engine)
        self._toolkit = LLMExplorerToolkit(
            db=self._database_connection, llm=self._llm, verbose=True
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history")

        self.SQL_PREFIX = """You are an agent designed to leverage the provided tools and datasets to answer at the best of your ability, question related to SQL databases focused on pyspark sql, but can handle any dialect.
        As an agent, you can solve both general questions that may or may not require access to the database, and specific questions that require access to the database, tools and external services. In any case, your goal is to answer the question as best as you can. 
        When you find out that you need to run SQL queries to create an answer, given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question. 
        When using pyspark/databricks sql dialtect, do not use double quotes to build your query's columns names -only if you are using a different dialect, or it is extremely necessary-.
        You have access to tools for interacting with the database.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
        You may use tools to run python or pyspark scripts that use the dataframes returned by the SQL queries.
        If your prompt is too long, you can break up the data in chunks and run the first analysist using the chunk with the most recent data.
        Avoid creating queries that require too many tokens to read, so always include filters and limits.
        Make sure the you dont pass the 4097 tokens limit

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        Return the results in a string formatting the code or dataframe in a way that is easy to read.
        """

        self.SQL_SUFFIX = """Begin!

        Question: {input}
        Thought: I should look at the tables in the database to see what I can query.
        {agent_scratchpad}"""

        self.FORMAT_INSTRUCTIONS = """Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question."""
        SUFFIX = """Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""

        self.agent_executor = create_sql_agent(
            llm=self._llm,
            toolkit=self._toolkit,
            verbose=True,
            prefix=self.SQL_PREFIX,
            suffix=self.SQL_SUFFIX,
            format_instructions=self.FORMAT_INSTRUCTIONS,
            top_k=10,
            max_iterations=15,
            max_execution_time=None,
            early_stopping_method="force",
        )

    def run(self, query):
        return self.agent_executor.run(query)
