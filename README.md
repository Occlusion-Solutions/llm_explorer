# Occlusion LLM Explorer

[![CodeQL](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/github-code-scanning/codeql) [![python-ci](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/python-ci.yml) [![python-cd](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/python-cd.yml/badge.svg)](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/python-cd.yml) [![PyPI version](https://badge.fury.io/py/llm-explorer.svg)](https://badge.fury.io/py/llm-explorer)

**Lakehouse Analytics &amp; Advanced ML**
![llm_explorer_sample](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/assets/11726633/f6a5753d-681c-418f-babb-0a2df74dd4d8)

## Setup

**Important** This package requires **Open AI & HuggingFace API key**. Remember to run from a folder with the `.streamlit/secrets.toml` file.
See [here](https://beta.openai.com/docs/developer-quickstart/your-api-keys) and [here](https://huggingface.co/docs/hub/quicktour.html#authentication) for more details.

### Quick Install

```shell
python -m pip install llm-explorer
```

```shell
llm_explorer
```

Initial load could take some time as it downloads the model and the tokenizer. Remember to include the secrets.toml file under .streamlit/ folder.

### Build from source

Clone the repository

```shell
git clone https://github.com/Occlusion-Solutions/llm_explorer.git
```

Install the package

``` shell
cd llm_explorer && make install
```

Run the package

```shell
llm_explorer
```

### Build manaually

After cloning, ceate a virtual environment

```shell
conda create -n llm_explorer python=3.10
conda activate llm_explorer
```

Install the requirements

```shell
pip install -r requirements.txt
```

Run the python installation

```shell
python setup.py install
llm_explorer
```

## Usage

Use the `demo@occlusion.solutions` user and `DEMO@occlusion` password to login.

The deployment requires a secrets.toml file created under .streamlit/:

```shell
touch .streamlit/secrets.toml
```

It should have a schema like this:

```toml
[connections.openai]
api_key="sk-..." # OpenAI API Key

[connections.huggingface]
api_key="shf_..." # HuggingFace API Key

[connections.databricks]
server_hostname="your databricks host"
http_path="http path under cluster JDBC/ODBC connectivity"
access_token="your databricks access token"
```

## Run Modes

### Chain

An assistant Query engine, that is asked naturally with table references and helps in the query generation. The execution of the queries is manual

### Agent

It uses the pandas agent to generate the queries and execute them. It is a more natural way of querying the data and it operates autonomously until it thinks it finds and answer.

### Chat

It uses the HuggingFace Transformers Agent chat to operate in a conversational way.

## Lakehouse Agent Sample

Agent is queried for the top 10 producing wells. It identifies the tables it has access to and understands that the request could be satified by the padalloc table. It then creates a query that returns the top 10 producing assets and return the results.

```shell

> Entering new AgentExecutor chain...

Observation: logs, wells
Thought: I should look at the schema of the microchip_logs and padalloc tables to see what columns I can use.

Action: schema_sql_db
Action Input: "wells"
Observation: DDL
Thought: I should query the padalloc table to get the top 10 producing wells.

Action: query_sql_db
Action Input: "SELECT WELL_CODE, SUM(PROD_GAS_VOLUME_MCF) AS total_gas_volume_mcf FROM padalloc GROUP BY WELL_CODE ORDER BY total_gas_volume_mcf DESC LIMIT 10"
Observation: results_dataframe
Thought: I now know the top 10 producing wells.

Final Answer: The top 10 producing wells are 1222344, 1212560, 1222345, 1212503, 1222335, 1222340, 1222338, 1222367, 1220189, and 1222352.

> Finished chain.
```

## Attribution

This is an adapted implementation from the GitHub repository. See the contibutions list for more details:

https://github.com/kaarthik108/snowChat