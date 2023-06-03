import streamlit as st
from streamlit import components


class UI:
    def __init__():
        ...

    def chat_md():
        st.markdown(
            '<div id="input-container-placeholder"></div>', unsafe_allow_html=True
        )
        components.v1.html(
            """
            <script>
            window.addEventListener('load', function() {
                const inputContainer = document.querySelector('.stTextInput');
                const inputContainerPlaceholder = document.getElementById('input-container-placeholder');
                inputContainer.id = 'input-container';
                inputContainerPlaceholder.appendChild(inputContainer);
                document.getElementById("input").focus();
            });
            </script>
            """,
            height=0,
        )

    def message_func(text, is_user=False):
        """
        This function is used to display the messages in the chatbot UI.

        Parameters:
        text (str): The text to be displayed.
        is_user (bool): Whether the message is from the user or the chatbot.
        key (str): The key to be used for the message.
        avatar_style (str): The style of the avatar to be used.
        """
        if is_user:
            avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortFlat&hairColor=Black&facialHairType=BeardLight&facialHairColor=Black&clotheType=Hoodie&clotheColor=DarkBlue&eyeType=Squint&eyebrowType=DefaultNatural&mouthType=Smile&skinColor=Light"
            message_alignment = "flex-end"
            message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"
            avatar_class = "user-avatar"
            st.write(
                f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                        <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%;">
                            {text}
                        </div>
                                <img src="{avatar_url}" class="{avatar_class}" alt="avatar" />

                    </div>
                    """,
                unsafe_allow_html=True,
            )
        else:
            avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=Hat&accessoriesType=Prescription02&facialHairType=BeardMajestic&facialHairColor=Platinum&clotheType=BlazerShirt&eyeType=Close&eyebrowType=SadConcerned&mouthType=Twinkle&skinColor=Brown"
            message_alignment = "flex-start"
            message_bg_color = "#71797E"
            avatar_class = "bot-avatar"
            st.write(
                f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                        <img src="{avatar_url}" class="{avatar_class}" alt="avatar" />
                        <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%;">
                            {text} \n </div>
                    </div>
                    """,
                unsafe_allow_html=True,
            )

    def styles():
        return """
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.0/css/all.min.css">

<style>
    #input-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        padding: 10px;
        background-color: white;
        z-index: 100;
    }
    h1 {
        font-family: 'Roboto Slab', serif;
    }
    .user-avatar {
        float: right;
        width: 40px;
        height: 40px;
        margin-left: 5px;
        margin-bottom: -10px;
        border-radius: 50%;
        object-fit: cover;
    }
    .bot-avatar {
        float: left;
        width: 40px;
        height: 40px;
        margin-right: 5px;
        border-radius: 50%;
        object-fit: cover;
    }
</style>
"""

    def sidebar():
        return """
# LLM Explorer

## Features

- **Natural Language Processing**: Understands your text queries and converts them into SQL and python queries
- **Instant Results**: Fetches data from Engines and displays the results quickly. Create Job Manifest for Orchestrated pipelines deployments
- **GEN AI models**: Uses OpenAI's GPT-4, langchain and vector search (into loaded documents for databases metadata & codebase) to generate queries for the lakehouse

Here are some example queries you can try with LLM Explorer:

- Forecast the next the 3 days of data from the time series in your memory
- What are the top 10 producing wells?
- What is the site with most wells and what are their production?

Streamlit is an open-source app framework built specifically for
Machine Learning and Data Science projects.
### Want to learn more?
- Check out [streamlit.io](https://streamlit.io)
- Jump into our [documentation](https://docs.streamlit.io)
- Ask a question in our [community
    forums](https://discuss.streamlit.io)
### See more complex demos
- Use a neural net to [analyze the Udacity Self-driving Car Image
    Dataset](https://github.com/streamlit/demo-self-driving)
- Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""


def about():
    return """
# LLM Base
***
This repository includes two initial execution modes. The python notebook is a direct implementation of the LLM agent, while the tse_llm_explorer is a python script to be executed with streamlit (streamit run tse_llm_explorer.py). The streamlit app is a simple interface to interact with the LLM agent.
***

This repository focuses on experimenting with the LangChain library for building powerful applications with large language models (LLMs). By leveraging state-of-the-art language models like OpenAI's GPT-3.5 Turbo (and soon GPT-4).

LangChain is a comprehensive framework designed for developing applications powered by language models. It goes beyond merely calling an LLM via an API, as the most advanced and differentiated applications are also data-aware and agnostic, enabling language models to connect with other data sources and interact with their environment. The LangChain framework is specifically built to address these principles.

## LangChain

The Python-specific portion of LangChain's documentation covers several main modules, each providing examples, how-to guides, reference docs, and conceptual guides. These modules include:

1. Models: Various model types and model integrations supported by LangChain.
3. Prompts: Prompt management, optimization, and serialization.
3. Memory: State persistence between chain or agent calls, including a standard memory interface, memory implementations, and examples of chains and agents utilizing memory.
4. Indexes: Combining LLMs with custom text data to enhance their capabilities.
5. Chains: Sequences of calls, either to an LLM or a different utility, with a standard interface, integrations, and end-to-end chain examples.
6. Agents: LLMs that make decisions about actions, observe the results, and repeat the process until completion, with a standard interface, agent selection, and end-to-end agent examples.

## Use Cases
With LangChain, developers can create various applications, such as customer support chatbots, automated content generators, data analysis tools, and intelligent search engines. These applications can help businesses streamline their workflows, reduce manual labor, and improve customer experiences.

## Service
By selling LangChain-based applications as a service to businesses, you can provide tailored solutions to meet their specific needs. For instance, companies can benefit from customizable chatbots that handle customer inquiries, personalized content creation tools for marketing, or internal data analysis systems that harness the power of LLMs to extract valuable insights. The possibilities are vast, and LangChain's flexible framework makes it the ideal choice for developing and deploying advanced language model applications in diverse industries.

## Requirements

- [Python 3.6 or higher](https://www.python.org/downloads/)
- [LangChain library](https://python.langchain.com/en/latest/index.html)
- [OpenAI API key](https://platform.openai.com/)
- [SerpAPI API Key](https://serpapi.com/)

## OpenAI API Models
The OpenAI API is powered by a diverse set of [models](https://platform.openai.com/docs/models) with different capabilities and price points. You can also make limited customizations to our original base models for your specific use case with fine-tuning.

## Installation

#### 1. Create a Python environment

Python 3.6 or higher using `venv` or `conda`. Using `venv`:

``` bash
cd tse-llm
python3 -m venv env
source env/bin/activate
```

Using `conda`:
``` bash
cd tse-llm
conda create -n tse-llm-env python=3.11
conda activate tse-llm-env
```

#### 3. Install the required dependencies
``` bash
pip install -r requirements.txt
```

#### 4. Set up the keys in a .env file

First, create a `.env` file in the root directory of the project. Inside the file, add your OpenAI API key:

```makefile
OPENAI_API_KEY=your_api_key_here
```

Save the file and close it. In your Python script or Jupyter notebook, load the `.env` file using the following code:
```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
```

By using the right naming convention for the environment variable, you don't have to manually store the key in a separate variable and pass it to the function. The library or package that requires the API key will automatically recognize the `OPENAI_API_KEY` environment variable and use its value.

When needed, you can access the `OPENAI_API_KEY` as an environment variable:
```python
import os
api_key = os.environ['OPENAI_API_KEY']
```

Now your Python environment is set up, and you can proceed with running the experiments.

## Run Streamlit App

You can run the app by running:

```bash
streamlit run explorer.py
```
            """
