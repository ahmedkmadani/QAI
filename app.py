from flask import Flask, render_template, request, jsonify  # Import render_template and jsonify
import openai
import os  # Import os for environment variables
from dotenv import load_dotenv  # Import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for API key

@app.route('/', methods=['GET', 'POST'])  # Allow POST method
def hello_world():  # put application's code here
    if request.method == 'POST':  # Check if the request method is POST
        title = request.form.get('bugTitle')  # Get the bug title from form data
        response = None  # Initialize response variable

        if title:  # Check if title is provided
            response = generate_bug_report(title)  # Call generate_bug_report with title

        return render_template('index.html', response=response, bugTitle=title)  # Pass response and title to template
    else:
        return render_template('index.html', response=None, bugTitle=None)  # Render template for GET requests

@app.route('/create_test_case', methods=['POST'])  # New endpoint for creating a test case
def create_test_case():
    title = request.form.get('bugTitle')  # Get the bug title from form data
    if title:
        test_case = generate_test_case(title)  # Call function to generate test case
        return jsonify(test_case)  # Return the generated test case as JSON
    return jsonify({"error": "Bug title is required"}), 400  # Return error if title is missing

def generate_bug_report(title):
    prompt = f"""
    You are a software testing assistant. Based on the following bug report title, generate the remaining bug report details in JSON format:
    
    Bug Report Title: {title}

    Format the response as:
    {{
        "description": "Your description here",
        "expected_result": "Your expected result here",
        "actual_result": "Your actual result here",
        "system_acceptance_criteria": [
            "Criteria 1",
            "Criteria 2"
        ]
    }}
    """
    
    # Call to ChatGPT API
    response = call_chatgpt_api(prompt)
    
    # Parse the response into JSON format
    return parse_bug_report_response(response)

def parse_bug_report_response(response):
    import json
    try:
        # Log the raw response for debugging
        # print("Raw response from ChatGPT API:", response)  # Debugging line
        
        # Remove Markdown formatting
        response = response.strip().split('\n', 1)[-1].strip('```json').strip('```').strip()
        
        return json.loads(response)
    except json.JSONDecodeError:
        return {"Error": "Failed to parse response into JSON", "Raw Response": response}  # Include raw response in error

def generate_test_case(title):
    prompt = f"""
    You are a software testing assistant. Based on the following bug report title, generate a test case in JSON format:
    
    Bug Report Title: {title}

    Format the response as:
    {{
        "test_case_id": "TC-001",
        "description": "Your test case description here",
        "steps": [
            "Step 1",
            "Step 2"
        ],
        "expected_result": "Your expected result here"
    }}
    """
    
    # Call to ChatGPT API
    response = call_chatgpt_api(prompt)
    
    # Parse the response into JSON format
    return parse_test_case_response(response)

def parse_test_case_response(response):
    import json
    try:
        # Log the raw response for debugging
        # print("Raw response from ChatGPT API:", response)  # Debugging line
        
        # Remove Markdown formatting
        response = response.strip().split('\n', 1)[-1].strip('```json').strip('```').strip()
        
        return json.loads(response)
    except json.JSONDecodeError:
        return {"Error": "Failed to parse response into JSON", "Raw Response": response}  # Include raw response in error

def call_chatgpt_api(prompt):
    try:  # Add error handling
        response = openai.ChatCompletion.create(  # Updated to use ChatCompletion
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}],  # Updated to use messages format
            temperature=0,
            max_tokens=500
        )
        return response.choices[0].message['content']  # Updated to access message content
    except Exception as e:  # Catch exceptions
        return f"Error: {str(e)}"  # Return error message

if __name__ == '__main__':
    app.run(debug=True)
