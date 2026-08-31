from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from schemas import QueryRequest, QueryResponse
from chain import ask  # wherever your ask() function actually lives

app = FastAPI(title="LogiFlow Docs Assistant")

@app.post("/ask", response_model=QueryResponse)
def ask_endpoint(request: QueryRequest):
    return ask(request.question)


# --- Simple built-in test UI, no separate frontend needed ---
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Docs Assistant</title></head>
        <body style="font-family: sans-serif; max-width: 700px; margin: 40px auto;">
            <h2>LogiFlow Docs Assistant</h2>
            <textarea id="question" rows="3" style="width: 100%;" placeholder="Ask a question..."></textarea>
            <br><br>
            <button onclick="ask()">Ask</button>
            <pre id="result" style="background: #f4f4f4; padding: 15px; white-space: pre-wrap;"></pre>

            <script>
                let sessionId = localStorage.getItem("session_id");
                if (!sessionId) {
                    sessionId = crypto.randomUUID();
                    localStorage.setItem("session_id", sessionId);
                }
                async function ask() {
                    const question = document.getElementById("question").value;
                    document.getElementById("result").textContent = "Loading...";
                    const res = await fetch("/ask", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({question: question, session_id: sessionId})
                    });
                    const data = await res.json();

                    let output = data.answer + "\\n\\n-----\\nsource :\\n";
                    data.sources.forEach(s => {
                        output += s.source_name + "\\n";
                    });
                    output += "\\nconfidence: " + data.confidence;

                    document.getElementById("result").textContent = output;
                }
            </script>
        </body>
    </html>
    """