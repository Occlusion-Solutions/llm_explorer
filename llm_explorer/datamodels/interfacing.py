# %%
from pydantic import BaseModel, Field
import streamlit as st


class StreamlitSessionState(BaseModel):
    agent_database: str = Field(
        default="default",
        description="Agent Database",
    )

    # iterate over all the class attributes and set them as streamlit session state
    def __init__(self, **data):
        super().__init__(**data)
        for k, v in data.items():
            st.session_state[k] = v

    # def set_state(self, **data):
    #     self.

    # def set_session(self,):
    #     if "agent_database" not in st.session_state:
    #         st.session_state["agent_database"] = self.agent_database


# %%


# #%%

# class SessionState(BaseModel):
#     databricks: bool = Field(
#         default=False,
#         description="Databricks Session State",
#     )
#     mlflow: bool = Field(
#         default=False,
#         description="MLFlow Session State",
#     )
#     snowpark: bool = Field(
#         default=False,
#         description="Snowpark Session State",
#     )
#     streamlit: bool = Field(
#         default=False,
#         description="Streamlit Session State",
#     )


# agent_database = (
#     st.session_state["agent_database"]
#     if "agent_database" in st.session_state
#     else "default"
# )

# def set_chat_state():
#     if "generated" not in st.session_state:
#         st.session_state["generated"] = [session_state_templates()["greeting"]]
#     if "past" not in st.session_state:
#         st.session_state["past"] = session_state_templates()["prior"]
#     if "input" not in st.session_state:
#         st.session_state["input"] = session_state_templates()["starting_query"]
#     if "stored_session" not in st.session_state:
#         st.session_state["stored_session"] = []
#     if "messages" not in st.session_state:
#         st.session_state["messages"] = [session_state_templates()["default_messages"]]
#     if "query_count" not in st.session_state:
#         st.session_state["query_count"] = 0
#     if "session_dataframe" not in st.session_state:
#         st.session_state["session_dataframe"] = None

#     chat_history = session_state_templates()["prior"]
#     MAX_INPUTS = 3


#     messages = st.session_state["messages"]


#     def run_chat_chain(chain, query, chat_history):
#     with st.spinner(text="Executing LLM Chain..."):
#         submit_progress_bar = st.empty()
#         messages = st.session_state["messages"]

#         # # Chroma Chain
#         # chroma_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
#         # chroma_vectorstore = VectorStoreHandler(**{"vectorstore":"chroma"}).get_vectorstore()
#         # chroma_result = chain.run({"question": query, "chat_history": chat_history}, chroma_vectorstore, chroma_memory)
#         # update_progress_bar(22, 'submit', submit_progress_bar)

#         # Faiss Chain

#         faiss_vectorstore = VectorStoreHandler(
#             **{"vectorstore": "faiss"}
#         ).get_vectorstore()
#         faiss_result = chain.run(
#             {"question": query, "chat_history": chat_history},
#             faiss_vectorstore,
#             faiss_memory,
#         )
#         update_progress_bar(44, "submit", submit_progress_bar)
#         result = validate_response(
#             faiss_result, chain, chat_history, faiss_vectorstore, enabled=False
#         )
#         update_progress_bar(66, "submit", submit_progress_bar)

#         chat_history.append(result)
#         messages.append((query, result))
#         st.session_state.generated.append(result)
#         update_progress_bar(88, "submit", submit_progress_bar)

#         st.session_state.past.append(query)
#         st.session_state["query_count"] += 1
#         update_progress_bar(100, "submit", submit_progress_bar)
#         return result, messages


#     messages_container:
#         if st.session_state["generated"]:
#             for i in range(len(st.session_state["generated"])):
#                 prior_query = st.session_state["past"][i]
#                 result_query = st.session_state["generated"][i]


#                  if st.session_state["query_count"] == MAX_INPUTS and RESET:


#                        st.session_state.messages.append((query, result))
#     st.session_state.past.append(query)
#     st.session_state.generated.append(result)

#     st.session_state["session_dataframe"] = df


#     if "llm" not in st.session_state:
#         st.session_state["llm"] = llm


#         @st.cache_data()
# def create_gpt_completion(ai_model: str, messages: List[dict]) -> dict:
#     try:
#         openai.api_key = st.secrets.api_credentials.api_key
#     except (KeyError, AttributeError):
#         st.error(st.session_state.locale.empty_api_handler)
#     logging.info(f"{messages=}")
#     completion = openai.ChatCompletion.create(
#         model=ai_model,
#         messages=messages,
#         # stream=True,
#         # temperature=0.7,
#     )
#     logging.info(f"{completion=}")
#     return completion


# def calc_cost(usage: dict) -> None:
#     total_tokens = usage.get("total_tokens")
#     prompt_tokens = usage.get("prompt_tokens")
#     completion_tokens = usage.get("completion_tokens")
#     st.session_state.total_tokens.append(total_tokens)
#     # pricing logic: https://openai.com/pricing#language-models
#     if st.session_state.model == "gpt-3.5-turbo":
#         cost = total_tokens * 0.002 / 1000
#     else:
#         cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
#     st.session_state.costs.append(cost)


#     # # Storing The Context
# # if "locale" not in st.session_state:
# #     st.session_state.locale = en
# # if "generated" not in st.session_state:
# #     st.session_state.generated = []
# # if "past" not in st.session_state:
# #     st.session_state.past = []
# # if "messages" not in st.session_state:
# #     st.session_state.messages = []
# # if "user_text" not in st.session_state:
# #     st.session_state.user_text = ""
# # if "input_kind" not in st.session_state:
# #     st.session_state.input_kind = st.session_state.locale.input_kind_1
# # if "seed" not in st.session_state:
# #     st.session_state.seed = 420# noqa: S311
# # if "costs" not in st.session_state:
# #     st.session_state.costs = []
# # if "total_tokens" not in st.session_state:
# #     st.session_state.total_tokens = []


# # Streamlit Datamodels


# # ML Flow Datamodels

# # Databricks Datamodels

# # Snowpark Datamodels
