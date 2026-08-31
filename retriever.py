from langchain_chroma import Chroma
from embeddings import get_embeddings

def retriever(user_input):
    """Retrieve the most relevant chunks from the vector store for a query.

Runs a similarity search against ChromaDB using the user's query,
returning each matching chunk alongside its similarity score so
downstream steps can filter low-confidence matches or build citations.

Args:
    user_input (str): The user's raw query/message to search against.

Returns:
    list[tuple[Document, float]]: Matching chunks paired with their
        similarity score, ordered by relevance (most relevant first).
"""
    emb = get_embeddings()

    vector_store = Chroma(
        persist_directory="chroma store",
        embedding_function=emb
    )
    results = vector_store.similarity_search_with_score(
        user_input, 
        k=3
        )
    filtered_results =  [(doc, score) for doc, score in results if score <= 0.7]
    return filtered_results