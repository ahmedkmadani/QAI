from flask import Flask, render_template, request  # Import render_template
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

        return render_template('index.html', response=response)  # Pass response to template
    else:
        return render_template('index.html', response=None)  # Render template for GET requests

def generate_bug_report(title):
    prompt = f"""
    You are helping to test software. Please fill in the details for a bug report. Use simple and clear language.

    Bug report title: {title}

    Fill in the following information:
    {{
        "title": "{title}",
        "description": "What happened? (Describe the issue)",
        "expected_result": "What should happen? (How should it work?)",
        "actual_result": "What actually happened? (What did you see?)",
        "reproduce_steps": [
            "Step 1: What is the first thing you did?",
            "Step 2: What did you do next?",
            // Add more steps if needed
        ],
        "system_acceptance_criteria": [
            "Criteria 1: What should the system do?",
            "Criteria 2: What else is required?",
            // Add more criteria if needed
        ]
    }}

    Please keep the description simple and clear.
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
