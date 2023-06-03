def session_state_templates():
    return {
        "greeting": "Welcome to the LLM Explorer 🔍 Please type you prompt in the text box below and hit submit to get started 🚀",
        "default_messages": """Hi, please type your query and I will help you creating: 
        - forecasts
        - job manifests
        - data analysis
        - insights from the lakehouse
        - package usage and functions development
        - and more!
        """,
        "query_form": "Please type you query here",
        "starting_query": "Which are the top 10 producing wells?",
        "prior": [
            "Hi, you are an developer assistant that will use the tools, memory vector stores and chat history to provide the most consistent answer to the user. I will prompt you to help me creating: \n - forecasts \n - job manifests \n - data analysis \n - insights from the lakehouse \n - package usage and functions development \n - and more. Let's think this step by step"
        ],
    }
