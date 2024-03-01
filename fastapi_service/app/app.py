from flask import Flask, request, jsonify
from flask_cors import CORS
from .services.llm import *

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    query = data['query']
    response = llm.handle_query(query)  # This function needs to handle both chat and suggestion requests

    # Check if the response should include suggestions
    # This assumes `handle_query` can return a response with a 'questions' key for suggestions
    return jsonify(response)

@app.route('/process_selection', methods=['POST'])
def process_selection():
    data = request.json
    user_input = data.get('userInput')
    original_questions = data.get('originalQuestions')  # Assuming this is passed back for context

    # Process the user input along with the original questions
    # This function needs to be defined in your llm module
    combined_response = llm.process_user_input(user_input, original_questions)

    return jsonify({"response": combined_response})

if __name__ == '__main__':
    app.run(debug=True)