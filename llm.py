import os
from dotenv import load_dotenv
load_dotenv()

from pydantic import SecretStr

from langchain_groq import ChatGroq

#laod groq apikey:
api_key = os.getenv("GROQ_API_KEY")

#initiate llm model:
def build_llm():
    """Initialize and return the LLM used by the chatbot assistant.

Configures the chat model (e.g. Groq's openai/gpt-oss-120b) with the
project's generation settings, so it's built once and reused across
the QA chain rather than re-instantiated on every query.

Args:
    None

Returns:
    BaseChatModel: The configured LLM instance, ready to be wrapped in
        a retrieval chain.
"""
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Check your .env file.")

    model = ChatGroq(
        model = "openai/gpt-oss-120b",
        temperature = 0,
        api_key = SecretStr(api_key)
    )
    return model

