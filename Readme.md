# LogiFlow Docs Assistant

A RAG-based support chatbot that answers questions from LogiFlow's API documentation — grounded strictly in the provided docs, with source citations, and an honest refusal when the answer isn't covered.

## What it does

- Answers customer support questions using only the ingested documentation (no hallucinated answers)
- Returns structured responses: answer, confidence level, and deduplicated source citations
- Remembers conversation context within a session (follow-up questions like "why is that lower?" work correctly)
- Refuses to answer when the relevant information isn't in the docs, instead of guessing

## Tech stack

- **LLM**: Groq (`openai/gpt-oss-120b`) via `langchain-groq`, structured output via `with_structured_output`
- **Vector store**: ChromaDB, cosine similarity, persisted locally
- **Embeddings**: HuggingFace (`sentence-transformers`, CPU), normalized
- **Framework**: FastAPI
- **Schemas**: Pydantic (ingestion metadata + API request/response validation)
- **Chunking**: `MarkdownHeaderTextSplitter` (structured docs), custom `Q:/A:` splitter (FAQ-style docs)

## Project structure

```
ingest.py       # loads docs, tags metadata, builds/persists the Chroma vector store
embeddings.py   # shared embedding model config (normalized, CPU)
llm.py          # Groq LLM configuration
retriever.py    # loads the persisted vector store, retrieves + filters relevant chunks
chain.py         # orchestration: retrieval -> prompt -> LLM -> structured response
schemas.py      # Pydantic models (SourceMetadata, QueryRequest, QueryResponse, SourceCitation)
app.py          # FastAPI app + built-in browser test UI
data/source/    # the 3 sample docs ingested by ingest.py
docs/           # project reference docs (metadata taxonomy, retrieval test cases)
```

See [`docs/doc_taxonomy.md`](docs/doc_taxonomy.md) for the metadata schema (`source_type`, `product_area`, etc.), and [`docs/sample_support_questions.md`](docs/sample_support_questions.md) for the retrieval test cases used to validate this project.

## Setup

1. Clone the repo and move into it:
   ```bash
   git clone https://github.com/Jridi1/logiflow-docs-assistant.git
   cd logiflow-docs-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your Groq API key — copy `.env.example` to `.env` and fill it in:
   ```bash
   cp .env.example .env
   ```
   ```
   GROQ_API_KEY=your_key_here
   ```
   (No quotes, no extra spaces around the `=`.)

## Running it

1. Build the vector store (run once, or whenever source docs change):
   ```bash
   python3 ingest.py
   ```

2. Start the API server:
   ```bash
   uvicorn app:app --reload
   ```

3. Open `http://127.0.0.1:8000/` in a browser for a simple built-in test UI, or `http://127.0.0.1:8000/docs` for the interactive API documentation (Swagger UI, auto-generated from the Pydantic schemas).

## API

**POST** `/ask`

Request body:
```json
{
  "question": "What's the rate limit on the bulk shipment endpoint?",
  "session_id": "some-uuid"
}
```

Response:
```json
{
  "answer": "The bulk shipment endpoint (`POST /v2/shipments/bulk`) is capped at 10 requests per minute, regardless of plan.",
  "is_answerable": true,
  "confidence": "high",
  "sources": [
    {
      "source_name": "API Reference — Rate Limits",
      "product_area": "rate_limits",
      "url": "https://docs.logiflow.io/rate-limits"
    }
  ]
}
```

`session_id` is generated and persisted client-side (localStorage in the demo UI) to enable follow-up questions within the same conversation.

## Retrieval validation notes

- Retrieval was tested against multiple phrasings of the same underlying question (e.g. "rate limit on bulk shipments" / "how many bulk requests per minute" / "why am I rate limited on bulk endpoint even on Enterprise") — all three consistently retrieve the same top chunks.
- Chroma's distance metric was explicitly set to cosine (`hnsw:space: cosine`) with normalized embeddings, rather than relying on the default L2 metric, for interpretable and consistent similarity scores.
- A similarity score threshold (0.7, cosine distance) filters out irrelevant retrieved chunks before they reach the LLM; if no chunks pass the threshold, the system returns `is_answerable: false` without calling the LLM.
- Semantic similarity (embedding-based) was evaluated as a way to test answer correctness, but was found unreliable for numeric facts specifically — a wrong number in an otherwise similarly-phrased sentence can score a *higher* similarity than the correct number, since embeddings weight sentence structure more than the specific digit. Exact-value / keyword-based checks are used instead where a specific fact (like a rate limit number) needs to be verified.

## Known limitations (by design, for this milestone)

- Session memory is in-process (a Python dict) — resets on server restart and does not scale across multiple server instances. A persistent store (e.g. Redis) is the planned upgrade for a later milestone.
- Only `api_reference`-type docs (the 3 sample pages) are fully ingested and tested end-to-end. FAQ-style content requires a different chunking strategy (implemented separately, not yet merged into the main ingestion path) since it lacks markdown headers to split on.
