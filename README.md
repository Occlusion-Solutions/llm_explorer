# Occlusion LLM Explorer

[![CodeQL](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/github-code-scanning/codeql) [![python-ci](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/python-ci.yml) [![python-cd](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/python-cd.yml/badge.svg)](https://github.com/Occlusion-Solutions/occlussion_llm_explorer/actions/workflows/python-cd.yml) [![PyPI version](https://badge.fury.io/py/llm-explorer.svg)](https://badge.fury.io/py/llm-explorer)


**Lakehouse Analytics &amp; Advanced ML**
![llm_explorer_sample.png](/docs/.attachments/llm_explorer_sample.png)

## Setup
**Important** This package requires **Open AI & HuggingFace API key**

### Pypi
```shell
python -m pip install llm-explorer
```

```shell
touch main.py
```

```python
from llm_explorer import main

if __name__ == "__main__":
    main()
```

```shell
python -m streamlit run main.py
```

Initial load could take some time as it downloads the model and the tokenizer. Remember to include the secrets.toml file under .streamlit/ folder.


### Build from source
Create a virtual environment

```shell
conda create -n occlusion python=3.10
conda activate occlusion
```

Install the requirements

```shell
pip install -r requirements.txt
```

Run the main.py script using streamlit:

```shell
python -m streamlit run main.py
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

## Lakehouse Agent Sample

Agent is queried for the top 10 producing wells. It identifies the tables it has access to and understands that the request could be satified by the padalloc table. It then creates a query that returns the top 10 producing assets and return the results.

```shell

> Entering new AgentExecutor chain...

Observation: microchip_logs, padalloc
Thought: I should look at the schema of the microchip_logs and padalloc tables to see what columns I can use.

Action: schema_sql_db
Action Input: "microchip_logs, padalloc"
Observation: 
CREATE TABLE `microchip_logs` (
        `file_path` STRING, 
        `content` STRING
)


CREATE TABLE `padalloc` (
        `ZONE_CODE` STRING, 
        `ZONE_NAME` STRING, 
        `ZONE_HID` DECIMAL, 
        `WELL_HID` DECIMAL, 
        `WELL_CODE` STRING, 
        `PROD_DATE` TIMESTAMP, 
        `PROD_GAS_VOLUME_MCF` DECIMAL, 
        `PROD_OIL_VOLUME_BBL` DECIMAL, 
        `PROD_WATER_VOLUME_BBL` DECIMAL, 
        `ALLOCATED_FLAG` STRING, 
        `SALE_GAS_VOLUME_MCF` DECIMAL, 
        `SALE_OIL_VOLUME_BBL` DECIMAL, 
        `LGL_VOLUME_MCF` DECIMAL, 
        `OTHER_USES_GAS_MCF` DECIMAL
)

Thought: I should query the padalloc table to get the top 10 producing wells.

Action: query_sql_db
Action Input: "SELECT WELL_CODE, SUM(PROD_GAS_VOLUME_MCF) AS total_gas_volume_mcf FROM padalloc GROUP BY WELL_CODE ORDER BY total_gas_volume_mcf DESC LIMIT 10"
Observation: [('1222344             ', Decimal('8429191.6172')), ('1212560             ', Decimal('8211108.4867')), ('1222345             ', Decimal('8163411.9976')), ('1212503             ', Decimal('6621501.8683')), ('1222335             ', Decimal('4773668.6216')), ('1222340             ', Decimal('4276560.8228')), ('1222338             ', Decimal('4153258.1434')), ('1222367             ', Decimal('4018012.2406')), ('1220189             ', Decimal('3965394.4453')), ('1222352             ', Decimal('3786076.4127'))]
Thought: I now know the top 10 producing wells.

Final Answer: The top 10 producing wells are 1222344, 1212560, 1222345, 1212503, 1222335, 1222340, 1222338, 1222367, 1220189, and 1222352.

> Finished chain.
```