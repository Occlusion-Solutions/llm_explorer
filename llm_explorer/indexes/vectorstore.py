import pandas as pd
import streamlit as st
from langchain.document_loaders import DataFrameLoader, UnstructuredMarkdownLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS, Chroma

embeddings = OpenAIEmbeddings(openai_api_key=st.secrets.connections.openai.api_key)


class VectorStoreHandler:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_vectorstore(self):
        get_vectorstore_strategies = {
            "chroma": load_chroma_vectorstore,
            "faiss": load_faiss_vectorstore,
        }
        vectorstore_strategy = self.kwargs.get("vectorstore", "chroma")
        return get_vectorstore_strategies[vectorstore_strategy]()

    def set_vectorstore(self):
        set_vectorstore_strategies = {
            "chroma": pandas_df_vectorstore_loader,
            "faiss": faiss_metadata_index_loader,
        }
        vectorstore_strategy = self.kwargs.get("vectorstore", "chroma")
        return set_vectorstore_strategies[vectorstore_strategy]()


@st.cache_resource
def load_chroma_vectorstore():
    return Chroma(persist_directory="llm_explorer/indexes/croma_index", embedding_function=embeddings)


@st.cache_resource
def load_faiss_vectorstore():
    return FAISS.load_local("llm_explorer/indexes/faiss_index", embeddings)


def faiss_metadata_index_loader(
    metadata_path: str = "llm_explorer/indexes/metadata/schema.md",
    page_content_column: str = "y",
):
    loader = UnstructuredMarkdownLoader(metadata_path)
    data = loader.load()
    # df = pd.read_csv(data_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    texts = text_splitter.split_documents(data)

    # df_loader = DataFrameLoader(df, page_content_column=page_content_column)
    # docs = df_loader.load()

    faiss_store = FAISS.from_documents(texts, embeddings)
    # docsearch.add_documents(docs)
    faiss_store.save_local("llm_explorer/indexes/faiss_index")

    # with open("vectors.pkl", "wb") as f:
    #     pickle.dump(docsearch, f)


def pandas_df_vectorstore_loader(
    data_path: str = "llm_explorer/indexes/samples/telemetry_sample_forecast.csv",
    page_content_column: str = "y",
):
    df = pd.read_csv(data_path)
    # jdf = df.to_dict(orient='split')
    loader = DataFrameLoader(df, page_content_column=page_content_column)
    docs = loader.load()

    # VectorStoreRetrieverMemory

    vectorstore_ts = Chroma.from_documents(
        docs, embeddings, persist_directory="croma_index"
    )
    # docs = pandas_df_vectorstore_loader(data_path=df_path,  page_content_column=data_columnn)
    vectorstore_ts.persist()

    return docs
