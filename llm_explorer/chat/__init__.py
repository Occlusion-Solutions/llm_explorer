import contextlib

import streamlit as st
from langchain.memory import ConversationBufferMemory

from llm_explorer.agents import ExplorerAgent, HFTAgent
from llm_explorer.chains import extract_code, is_sql_query
from llm_explorer.databases.adbddl import ADBDDL
from llm_explorer.indexes.vectorstore import VectorStoreHandler
from llm_explorer.llm import set_llm
from llm_explorer.templates.chains import chains_templates
from llm_explorer.templates.ui import session_state_templates
from llm_explorer.ui import UI

set_llm()

adb_ddl = ADBDDL()
agent_database = (
    st.session_state["agent_database"]
    if "agent_database" in st.session_state
    else "default"
)
explorer_agent = ExplorerAgent(**{"database": agent_database})
hft_agent = HFTAgent()
faiss_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def update_progress_bar(value, prefix, progress_bar=None):
    if progress_bar is None:
        progress_bar = st.empty()

    key = f"{prefix}_progress_bar_value"
    if key not in st.session_state:
        st.session_state[key] = 0

    st.session_state[key] = value
    progress_bar.progress(st.session_state[key])
    if value == 100:
        st.session_state[key] = 0
        progress_bar.empty()


def set_chat_state():
    if "generated" not in st.session_state:
        st.session_state["generated"] = [session_state_templates()["greeting"]]
    if "past" not in st.session_state:
        st.session_state["past"] = session_state_templates()["prior"]
    if "input" not in st.session_state:
        st.session_state["input"] = session_state_templates()["starting_query"]
    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []
    if "messages" not in st.session_state:
        st.session_state["messages"] = [session_state_templates()["default_messages"]]
    if "query_count" not in st.session_state:
        st.session_state["query_count"] = 0
    if "session_dataframe" not in st.session_state:
        st.session_state["session_dataframe"] = None

    chat_history = session_state_templates()["prior"]
    MAX_INPUTS = 3

    return chat_history, MAX_INPUTS


def validate_response(response, chain, chat_history, vectorstore, enabled=False):
    if enabled:
        # # Faiss Chain Validation
        validation_faiss_memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        validation_query = f"{chains_templates()['validation_prompt']} \n {response}"
        return chain.run(
            {"question": validation_query, "chat_history": chat_history},
            vectorstore,
            validation_faiss_memory,
        )
    else:
        return response


def run_chat_chain(chain, query, chat_history):
    with st.spinner(text="Executing LLM Chain..."):
        submit_progress_bar = st.empty()
        messages = st.session_state["messages"]

        # # Chroma Chain
        # chroma_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        # chroma_vectorstore = VectorStoreHandler(**{"vectorstore":"chroma"}).get_vectorstore()
        # chroma_result = chain.run({"question": query, "chat_history": chat_history}, chroma_vectorstore, chroma_memory)
        # update_progress_bar(22, 'submit', submit_progress_bar)

        # Faiss Chain

        faiss_vectorstore = VectorStoreHandler(
            **{"vectorstore": "faiss"}
        ).get_vectorstore()
        faiss_result = chain.run(
            {"question": query, "chat_history": chat_history},
            faiss_vectorstore,
            faiss_memory,
        )
        update_progress_bar(44, "submit", submit_progress_bar)
        result = validate_response(
            faiss_result, chain, chat_history, faiss_vectorstore, enabled=False
        )
        update_progress_bar(66, "submit", submit_progress_bar)

        chat_history.append(result)
        messages.append((query, result))
        st.session_state.generated.append(result)
        update_progress_bar(88, "submit", submit_progress_bar)

        st.session_state.past.append(query)
        st.session_state["query_count"] += 1
        update_progress_bar(100, "submit", submit_progress_bar)
        return result, messages


def show_chat_buttons() -> None:
    b0, b1 = st.columns(2)
    with b0, b1:
        reset_button = b0.button("Reset Chat History")
        save_button = b1.download_button(
            label="Save Chat History",
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )
    return reset_button, save_button


def chat_loop(chain):
    chat_history, MAX_INPUTS = set_chat_state()

    RESET = True
    messages_container = st.container()

    with st.form(key="tse_chat_form"):
        query = st.text_area(
            "Query: ",
            key="input",
            value="",
            placeholder=session_state_templates()["query_form"],
            label_visibility="hidden",
            height=150,
        )
        submit_button = st.form_submit_button(label="Submit")

    reset_button, save_button = show_chat_buttons()

    # col1, col2 = st.columns([1, 3.2])

    if reset_button or st.session_state["query_count"] >= MAX_INPUTS and RESET:
        RESET = False
        st.session_state["query_count"] = 0
        set_chat_state()

    selection = st.select_slider(
        "Select an interaction mode",
        options=["chain", "agent", "chat"],
        value=("agent"),
    )
    st.write("You selected ", selection)

    if selection == "chain":
        ## Call LLM Api and Generate Results
        if len(query) > 2 and submit_button:
            result, messages = run_chat_chain(
                chain=chain, query=query, chat_history=chat_history
            )

    elif selection == "agent":
        ## Call Agent Api and Generate Results
        if len(query) > 2 and submit_button:
            with st.spinner(text="Executing LLM Agent..."):
                result = str(explorer_agent.run(query))
                update_chat_state(query, result)
    elif selection == "chat":
        ## Call Chat Api and Generate Results
        if len(query) > 2 and submit_button:
            with st.spinner(text="Executing LLM Chat..."):
                result = hft_agent.chat(query)
                update_chat_state(query, result)

    with messages_container:
        if st.session_state["generated"]:
            for i in range(len(st.session_state["generated"])):
                prior_query = st.session_state["past"][i]
                result_query = st.session_state["generated"][i]

                UI.message_func(prior_query, is_user=True)
                UI.message_func(result_query)
                try:
                    if i > 0 and is_sql_query(result_query):
                        code, run_query = run_generated_code(result_query)
                except Exception as e:
                    print(e)

    if st.session_state["query_count"] == MAX_INPUTS and RESET:
        st.warning(
            "You have reached the maximum number of inputs. The chat history will be cleared after the next input."
        )

    # col2.markdown(f'<div style="line-height: 2.5;">{st.session_state["query_count"]}/{MAX_INPUTS}</div>', unsafe_allow_html=True)

    UI.chat_md()


def update_chat_state(query, result):
    st.session_state.messages.append((query, result))
    st.session_state.past.append(query)
    st.session_state.generated.append(result)


def run_generated_code(result_query):
    code = extract_code(result_query)
    user_query = st.text_area(
        label=f"Run Query: {code}:", value=code, height=200, label_visibility="hidden"
    )
    run_query = st.button(label=f"Run Query: {user_query}")
    with contextlib.suppress(Exception):
        if code and run_query:
            with st.spinner(text="Running SQL Query..."):
                df = adb_ddl.query_lakehouse(user_query)
                st.session_state["session_dataframe"] = df
                print(df)
                st.dataframe(df, use_container_width=True)
    return code, run_query
