# Gemini Chatbot

This repository contains a Flask-based chatbot application built using the Gemini API. The chatbot has two main modules:

1. **Web UI (/):**

- Summarizes content based on a given title.

- Allows users to ask questions via a user interface.

2. **GraphQL Endpoint (/graphql):**

- Demonstrates backend query handling with GraphQL.

## Features

- Content Summarization: Summarizes content using the Gemini language model.
- Question-Answering: Answers user-provided questions by querying the Gemini API.
- GraphQL Playground: Interactive UI to test GraphQL queries.
- CORS Support: Configured for cross-origin resource sharing.

## Requirements
- Python 3.8 or higher
- Flask
- Requests
- Ariadne
- Flask-CORS
- Python Dotenv

## Setup
### Prerequisites
1. Obtain an API key for the Gemini application and store it in a .env file in the project root. The .env file should look like this:
```Python
API_KEY=your_gemini_api_key_here
```
2. Install python dependies:
```bash
pip install flask requests ariadne flask-cors python-dotenv
```

### Directory Structure
Ensure the following directory structure for static files and templates:
```bash
project_root/
|-- static/
|   |-- app.js
|
|-- templates/
|   |-- index.html
|
|-- .env
|-- app.py
```

### Running the Application
1. Start the Flask server:
   ```bash
    python app.py
    ```
2. Open your browser and navigate to http://127.0.0.1:5000 to access the web UI.
3. To test GraphQL queries, visit http://127.0.0.1:5000/graphql.

## GraphQL Queries
### Available Queries
1. askQuestion: Ask a question and receive a response.
  - Parameters: question (String!)
  - Example:
  - ```GraphQL
    query {
    askQuestion(question: "What is the weather today?")
    }
    ```

2. summarizeContent: Summarize content based on a given title.
 - Parameters: title (String!)
 - Example:
 - ```GraphQL
   query {
   summarizeContent(title: "Artificial Intelligence")
   }
   ```

## Files
1. **app.py:** The main Flask application file that handles API requests and GraphQL queries.
2. **static/app.js:** JavaScript logic for the web UI.
3. **templates/index.html:** HTML structure for the web UI.
4. **.env:** Environment variables file containing the API key.

## Dependencies
- **Flask**: Web framework for building the chatbot application.
- **Ariadne**: GraphQL library for Python.
- **Flask**-CORS: CORS support for Flask.
- **Requests**: HTTP requests handling.
- **Python Dotenv**: Loading environment variables.


## API Integration
The chatbot interacts with the Gemini API via the following endpoint:
```Python
https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent
```
### Request Format
```GraphQL
{
  "contents": [
    {
      "parts": [
        {
          "text": "Your prompt here"
        }
      ]
    }
  ]
}
```
### Response Format
```GraphQL
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Response text here"
          }
        ]
      }
    }
  ]
}
```
## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Gemini API: For providing the language model.
- Ariadne: For GraphQL query handling.




