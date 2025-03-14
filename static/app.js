const graphqlEndpoint = "http://127.0.0.1:5000/graphql";

async function sendGraphQLQuery(query, variables) {
    try {
        const response = await fetch(graphqlEndpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query, variables })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}. Details: ${errorText}`);
        }

        const result = await response.json();

        if (Array.isArray(result)) {
            return result[1]?.data || null;
        }
        return result.data;
    } catch (error) {
        console.error("Error:", error);
        return { error: "An error occurred while fetching data." };
    }
}

function renderMarkdownToHTML(text) {
    // Convert **bold** to <b>bold</b>
    text = text.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
    
    // Remove stray asterisks that are not part of valid Markdown
    text = text.replace(/(^|\s)\*(\s|$)/g, "$1$2");
    
    return text;
}

async function askQuestion() {
    const question = document.getElementById("questionInput").value;
    const query = `
                query ($question: String!) {
                    askQuestion(question: $question)
                }
            `;
    const data = await sendGraphQLQuery(query, { question });

    const questionResponseElement = document.getElementById("questionResponse");
    if (data && data.askQuestion) {
        questionResponseElement.innerHTML = renderMarkdownToHTML(data.askQuestion);
    } else {
        questionResponseElement.innerText = data ? data.error : "Error: No response from server.";
    }
}

async function summarizeContent() {
    const title = document.getElementById("titleInput").value;
    const query = `
                query ($title: String!) {
                    summarizeContent(title: $title)
                }
            `;
    const data = await sendGraphQLQuery(query, { title });

    const summaryResponseElement = document.getElementById("summaryResponse");
    if (data && data.summarizeContent) {
        summaryResponseElement.innerHTML = renderMarkdownToHTML(data.summarizeContent);
    } else {
        summaryResponseElement.innerText = data ? data.error : "Error: No response from server.";
    }
}

function handleEnter(event, action) {
    if (event.key === "Enter") {
        if (action === "ask") {
            askQuestion();
        } else if (action === "summarize") {
            summarizeContent();
        }
    }
}
