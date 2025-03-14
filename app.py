
from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from ariadne import gql, make_executable_schema, QueryType
from ariadne import graphql_sync
from flask_cors import CORS
from dotenv import load_dotenv

#loading .env file with API key
load_dotenv()

#API loaded
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("API_KEY") 
API_KEY =  os.getenv("API_KEY")  
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
print("Loaded API Key:", API_KEY)

#query handling
def query_gemini(prompt):
    try:
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        response = requests.post(ENDPOINT, json=data, headers=headers, params={"key": API_KEY})

        if response.status_code == 200:
            response_data = response.json()
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {response.status_code}, {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

#Query model defining
type_defs = gql("""
type Query {
    askQuestion(question: String!): String!
    summarizeContent(title: String!): String!
}
""")

query = QueryType()


@query.field("askQuestion")
def resolve_ask_question(_, info, question):
    return query_gemini(question)

@query.field("summarizeContent")
def resolve_summarize_content(_, info, title):
    prompt = f"Summarize the content with the title: {title}"
    return query_gemini(prompt)

schema = make_executable_schema(type_defs, query)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})



#For out HTML and app.js page
@app.route("/")
def index():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'index.html')


#Defined for GraphQL
playground_html = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
    <script src="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
</head>
<body>
    <div id="root"></div>
    <script>
        window.addEventListener('load', function () {
            GraphQLPlayground.init(document.getElementById('root'), { endpoint: '/graphql' })
        })
    </script>
</body>
</html>
"""





#For PLAYGROUND HTML handling (GraphQL)
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return playground_html, 200

#Sending GraphQL query to LLM
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    print("Received query:", data) 
    
    result = graphql_sync(schema, data)
    print("GraphQL result:", result)

    if "errors" in result:
        return jsonify({"errors": result["errors"]}), 400

    return jsonify(result), 200


#Using app.js from static folder
@app.route("/static/<path:filename>")
def send_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == "__main__":
    app.run(debug=True)
