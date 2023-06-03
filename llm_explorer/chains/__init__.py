import re

import openai
import pandas as pd
import streamlit as st
from langchain.chains import ConversationalRetrievalChain, LLMChain, RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.prompt import PromptTemplate

from llm_explorer.llm import set_llm

set_llm()

from llm_explorer.templates.chains import chains_templates


def set_chain(llm, **kwargs):
    condense_question_prompt = PromptTemplate.from_template(
        chains_templates()["snowchat_chain_template"]
    )
    QA_PROMPT = PromptTemplate(
        template=chains_templates()["snowchat_prompt_template"],
        input_variables=["question", "context"],
    )

    question_generator = LLMChain(llm=llm, prompt=condense_question_prompt)

    doc_chain = load_qa_chain(
        llm=llm,
        chain_type=kwargs.get(
            "chain_type", "stuff"
        ),  # Should be one of "stuff","map_reduce", "map_rerank", and "refine".
        prompt=QA_PROMPT,
    )
    return question_generator, doc_chain


class ExplorerConversationChain:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.llm = set_llm()
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=st.secrets.connections.openai.api_key
        )

    def get_qa_retrieval_chain(self, vectorstore):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type=self.kwargs.get("chain_type", "stuff"),
            retriever=vectorstore.as_retriever(),
        )

    def get_chat(self, vectorstore, memory):
        question_generator, doc_chain = set_chain(self.llm)
        return ConversationalRetrievalChain(
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            combine_docs_chain=doc_chain,
            question_generator=question_generator,
        )

    # def load_state(self):
    #     memory = ConversationBufferMemory(
    #         memory_key="chat_history", return_messages=True
    #     )
    #     return ConversationalRetrievalChain.from_llm(
    #         OpenAI(temperature=0.8),
    #         self.vectorstore.as_retriever(search_kwargs={"k": 3}),
    #         memory=memory,
    #     )

    def run(self, prompt, vectorstore, memory):
        chain = self.get_chat(vectorstore, memory)
        return chain.run(prompt)


# can be removed with better prompt
def extract_code(text) -> str:
    # from langchain.chat_models import ChatOpenAI
    """
    This function is used to extract the SQL code from the user's input.

    Parameters:
    text (str): The text to be processed.

    Returns:
    str: The SQL code extracted from the user's input.
    """
    if len(text) < 5:
        return None
    # Use OpenAI's GPT-3.5 to extract the SQL code
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": chains_templates()["code_extraction_prompt"].format(
                    text=text
                ),
            },
        ],
        # stream=True
    )

    # Extract the SQL code from the response
    sql_code = response.choices[0].message.content

    return sql_code


def is_sql_query(text: str) -> bool:
    """
    Checks if the input text is likely an SQL query.

    :param text: input text
    :return: True if the input is likely an SQL query, False otherwise
    """
    # Define a list of common SQL keywords
    keywords = [
        "SELECT",
        "FROM",
        "WHERE",
        "UPDATE",
        "INSERT",
        "DELETE",
        "JOIN",
        "GROUP BY",
        "ORDER BY",
        "HAVING",
        "LIMIT",
        "OFFSET",
        "UNION",
        "CREATE",
        "ALTER",
        "DROP",
        "TRUNCATE",
        "EXPLAIN",
        "WITH",
    ]

    # Create a single regular expression pattern to search for all keywords
    pattern = r"\b(?:" + "|".join(keywords) + r")\b"

    # Check if any of the keywords are present in the input text (case-insensitive)
    if re.search(pattern, text, re.IGNORECASE):
        return True

    return False
