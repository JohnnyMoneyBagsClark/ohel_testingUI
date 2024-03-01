# tools.py
tools_list = [
    {
        "type": "function",
        "function": {
            "name": "elasticsearch_lookup",
            "description": "Query the ElasticSearch database to retrieve product information",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {
                        "type": "string",
                        "description": "The search term to look up in the ElasticSearch database. The search will be performed across all fields of the documents."
                    }
                },
                "required": ["search_query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "duckduckgo_search",
            "description": "Perform a web search using DuckDuckGo to find product information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for the web"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_fauna_db",
            "description": "Post new information to the FaunaDB",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data to be updated in the database"
                    }
                },
                "required": ["data"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "generate_questions_and_suggestions",
            "description": "Generate relevant questions and suggestions based on the user's query or context which is answered by the user on the front end of web app",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_query": {
                        "type": "string",
                        "description": "The user's query or context to generate questions and suggestions from"
                    }
                },
                "required": ["user_query"]
            }
        }
    }
]