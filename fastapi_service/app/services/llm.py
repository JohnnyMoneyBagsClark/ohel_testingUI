import os
import getpass
import time
import re
import json
from openai import OpenAI
from ddg_search import duckduckgo_search
from dotenv import load_dotenv
from faunadb_client import get_fauna_client
from faunadb import query as q
from ..utils.tools import tools_list
from elasticsearch import Elasticsearch

# Load environment variables from .env file
load_dotenv()


# Retrieve OpenAI API key from environment variables
open_ai_key = os.getenv('open_ai_key')

# Set the OpenAI API key in the environment
os.environ["OPENAI_API_KEY"] = open_ai_key


# Retrieve variables from .env file
elasticsearch_url = os.getenv('ELASTICSEARCH_URL')
elasticsearch_api_key = os.getenv('ELASTICSEARCH_API_KEY')
if not elasticsearch_url or not elasticsearch_api_key:
    raise ValueError("Elasticsearch URL or API key missing in environment variables.")


es_client = Elasticsearch(
    elasticsearch_url,
    headers={"Authorization": "ApiKey " + elasticsearch_api_key}
)


# Initialize FaunaDB client
fauna_client = get_fauna_client()

# Example operation: fetch a document by its reference from the fauna db
#result = fauna_client.query(q.get(q.ref(q.collection('Products'), '384967684936171593')))
#print(result)


response = es_client.info()
print(response)
#t



def elasticsearch_lookup(search_query):
    if not search_query:
        print("Empty search query")
        return []

    try:
        # Search across all indices
        index_name = "_all"

        print(f"SEARCHING '{search_query}' ACROSS ALL RELEVANT FIELDS")
        search_body = {
            "query": {
                "multi_match": {
                    "query": search_query,
                   # "fields": ["*"],  # Search across all fields
                    "fields": ["product.title"],  # Specify relevant fields
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            },
            "size": 3,  # Limit to top 3 matches
            "_source": ["*"]   # Retrieve full document content
        }

        response = es_client.search(index=index_name, body=search_body)
        hits = response["hits"]["hits"]

        if hits:
            results_text = "Search Results:\n"
            for hit in hits:
                item = hit["_source"]
                # Extract and format the fields from the item
                item_text = json.dumps(item, indent=2)  # Formats the item as a JSON string
                results_text += f"{item_text}\n\n"
        else:
            print("No results found")
            return "No results found"

    except Exception as e:
        print(f"An error occurred during Elasticsearch search: {e}")
        return '[]'  # Return empty JSON array as a string

    return results_text

'''
def duckduckgo_search(query):
    try:
        # If ddg_search has a function named 'search'
        results = ddg_search.search(query)
        # Convert results to string if necessary
        return json.dumps(results) if results else 'No results found'
    except AttributeError:
        print("Error: 'search' function not found in ddg_search module")
        return '[]'  # Return empty JSON array as string
'''

# Placeholder for FaunaDB update tool
def update_fauna_db(data):
    try:
        update_result = fauna_client.query(
            q.create(q.collection('YourCollection'), {"data": data})
        )
        return json.dumps(update_result)  # Convert result to JSON string
    except Exception as e:
        print(f"An error occurred: {e}")
        return '{}'  # Return empty JSON object as string











# Initialize OpenAI client
client = OpenAI()

#initializes a client, and creates an assistant using the OpenAI API. It then stores the assistant's ID.
# Instructions modified for clarity in extracting arguments from user queries
assistant = client.beta.assistants.create(
    name="Shopping Expert Assistant",
    #instructions="You are an intelligent personal assistant dedicated to understanding and fulfilling your clients' specific needs. Your primary goal is to recommend products that align closely with the client's requests. When a client specifies a product, your first step is to consult the FaunaDB database to check for detailed information on that item. If the database lacks sufficient details or if the item is not found, you are then required to utilize web search tools to find the product online, focusing on the best price or other specified criteria. Ensure accuracy and relevance in your responses, and prioritize client satisfaction in every interaction.",
    instructions="""You are OhShop, a sophisticated AI trained by OHEL TECHNOLOGIES, designed to assist with product shopping. Your capabilities include identifying products, researching, and recommending options based on user preferences.
Tools:

Elasticsearch Lookup: Use this tool for initial product searches. Input the identified product name into the 'search_query' field.
DuckDuckGo Search: If Elasticsearch Lookup yields insufficient data, use this tool with an optimized query for more comprehensive search results.
generate_questions_and_suggestions: function to be used any time you want to extract more information related to product details from the user query. This function will give you more information on product preferences from the user autmoatically
Python: Utilize Python for any data analysis or calculation tasks.
Browser: Engage this tool for real-time information, unfamiliar terms, or when explicitly requested to browse or provide links.
Procedure:

// 1.Identify Product: Engage with the user to determine their desired product. This can range from vague to specific. For users unsure of what they want, such as those looking for a gift, ask guiding questions to narrow down preferences.
    When a question is asked that requires user input, you MUST USE the generate_questions_and_suggestions to gather intel, then you will recieve some questions the user answer about their query
// 2. Determine Product Attributes: Once a product is identified, consider the attributes crucial for making the right choice. If unfamiliar with the product type, use DuckDuckGo Search to gather necessary information. Then, ask the user only the essential questions to guide your search.
// 3.Product Search:
    Use Elasticsearch Lookup first with 'search_query' as the product name.
    If insufficient, turn to DuckDuckGo Search with an optimized query for the desired product.
// 4.Product Recommendation: Present your findings in a persuasive manner, detailing why the selected product is the best choice for the user. Highlight key features and benefits relevant to the user's needs.
// 5.Continuous Assistance: Keep assisting the user as needed, utilizing all available resources and tools.""",
    tools=tools_list,
    model="gpt-4-1106-preview",
)
assistant_id = assistant.id
    # Create a new thread for the OpenAI Assistant
thread = client.beta.threads.create()


def handle_query(query):
    if query.lower() == 'exit':
        return {'response': 'Goodbye!'}

    try:
        thread = client.beta.threads.create()
        thread_id = thread.id
        client.beta.threads.messages.create(thread_id=thread_id, role="user", content=query)

        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
        run_id = run.id

        for _ in range(10):  # Wait up to 50 seconds
            time.sleep(5)
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                response_content = [msg.content[0].text.value for msg in messages.data if msg.role == "assistant"]
                print ('Sending response to front end', response_content)
                return {'response': response_content[-1]} if response_content else {'response': 'No response from assistant.'}

            elif run_status.status == 'requires_action':
                required_actions = run_status.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for action in required_actions:
                    func_name = action.function.name
                    print("USING FUNCTION " + func_name)

                    arguments = json.loads(action.function.arguments)

                    if func_name == "elasticsearch_lookup":
                        tool_outputs.append(handle_elasticsearch_lookup(action, arguments))

                    elif func_name == "duckduckgo_search":
                        tool_outputs.append(handle_duckduckgo_search(action, arguments))

                    elif func_name == "generate_questions_and_suggestions":
                        tool_outputs.append(handle_generate_questions_and_suggestions(action, arguments))

                client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs)

            else:
                print("Waiting for the Assistant to process...")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'response': 'An error occurred while processing the request.'}

    return {'response': 'Request processing incomplete.'}

def handle_elasticsearch_lookup(action, arguments):
    search_query = arguments.get('search_query')
    query_result = elasticsearch_lookup(search_query)  # This function needs to be defined elsewhere
    output_str = json.dumps(query_result) if query_result else 'No results found'
    return {"tool_call_id": action.id, "output": output_str}

def handle_duckduckgo_search(action, arguments):
    search_query = arguments.get('query')
    search_results = duckduckgo_search(search_query)  # This function needs to be defined elsewhere
    return {"tool_call_id": action.id, "output": search_results}

def handle_generate_questions_and_suggestions(action, arguments):
    try:
        user_query = arguments.get('user_query')
        questions_with_suggestions = generate_questions_and_suggestions(user_query)
        if not questions_with_suggestions:
            questions_with_suggestions = [{'question': 'No questions available.', 'suggestions': ["No suggestions available."]}]
        output_for_frontend = {
            "questions": questions_with_suggestions
        }
        output_json = json.dumps(output_for_frontend)
        print("Sending to frontend:", output_json)  # This will print the JSON to the terminal
        return {"tool_call_id": action.id, "output": json.dumps(output_for_frontend)}
    except Exception as e:
        print(f"An error occurred in handle_generate_questions_and_suggestions: {e}")
        return {"tool_call_id": action.id, "output": json.dumps({"questions": []})}

    '''return {"tool_call_id": action.id, "output": output_json}'''

def process_user_input(user_input, original_questions):
    # Combine user input with the original context and questions
    # This is a placeholder for the actual implementation, which will depend on your specific requirements
    combined_input = f"User input: {user_input}\nOriginal Questions: {original_questions}"
    return combined_input





'''
output_for_frontend = {
        "questions": [
            {
                "text": item['question'],
                "suggestions": item['suggestions']
            }
            for item in questions_with_suggestions
        ]
    }'''

#more functions to move

def generate_questions(prompt, max_questions=5):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate {max_questions} unique questions based on the following information: {prompt}"}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        # Accessing the response text correctly
        if response.choices:
            message_content = response.choices[0].message.content  # Corrected access to 'content'
            questions = message_content.strip().split('\n')
            return [question for question in questions if question]  # Filter out empty strings
        else:
            return ["No questions generated."]  # Return a default message if no questions
    except Exception as e:
        print(f"An error occurred while generating questions: {e}")
        return ["An error occurred while generating questions."]

def generate_suggestions_for_question(question):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Provide three suggestions for the following question: {question}"}
            ],
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5
        )
        # Accessing the response text correctly
        if response.choices:
            message_content = response.choices[0].message.content  # Corrected access to 'content'
            suggestions = message_content.strip().split(',')
            return {'question': question, 'suggestions': [suggestion.strip() for suggestion in suggestions]}
        else:
            return {'question': question, 'suggestions': ["No suggestions available."]}  # Default message
    except Exception as e:
        print(f"An error occurred while generating suggestions for the question: '{question}': {e}")
        return {'question': question, 'suggestions': ["An error occurred while generating suggestions."]}


    
def generate_questions_and_suggestions(prompt):
    questions = generate_questions(prompt)
    questions_and_suggestions = []

    for question in questions:
        question_and_suggestions = generate_suggestions_for_question(question)
        questions_and_suggestions.append(question_and_suggestions)

    return questions_and_suggestions