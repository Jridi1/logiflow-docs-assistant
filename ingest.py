import time
from functools import wraps


from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

from langchain_chroma import Chroma

from embeddings import get_embeddings


#Initiate embedding model:
emb = get_embeddings()

def timed(func):
    """Log how long a function call takes.

    Wraps a function so that, on every call, it prints the elapsed
    wall-clock time from start to finish, without changing the
    function's return value.

    Args:
        func (Callable): The function to wrap.

    Returns:
        Callable: The wrapped function, timing-instrumented.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[{func.__name__}] took {end - start:.3f}s")
        return result
    return wrapper

SourceType = Literal["api_reference", "faq", "changelog", "slack_thread"]
ProductArea = Literal["auth", "rate_limits", "errors", "shipments", "webhooks", "tracking"]


class SourceMetadata(BaseModel):
    """Metadata attached to a retrieved source, used for citations.

    """
    source_name: str= Field(..., description="Identifier of the originating document/source.")
    source_type: SourceType= Field(..., description="Category of the source (e.g. PDF, webpage, FAQ).")
    product_area: ProductArea = Field(..., description="Business/product domain this source belongs to.")
    url: str = Field(..., description="Link to the original source document.")
    last_updated: date = Field(..., description="Date the source content was last revised.")
@timed
def load_data():
    """Load raw source documents from the configured data directory.

This is the ingestion entry point: it reads files from disk (PDF/etc.)
and returns them as LangChain Document objects, unsplit and untagged.
Chunking and metadata tagging happen in later steps.

Args:
    None

Returns:
    list[Document]: Raw documents, one per loaded file/page, before
        splitting or metadata tagging.
"""
    loader = DirectoryLoader("data/source",
                             loader_cls = TextLoader)
    documents = loader.load()

    file_metadata = {
        "01_authentication.md": {
            "source_name": "API Reference — Authentication",
            "source_type": "api_reference",
            "product_area": "auth",
            "url": "https://docs.logiflow.io/auth",
            "last_updated": "2026-06-01",
        },
        "02_rate_limits.md": {
            "source_name": "API Reference — Rate Limits",
            "source_type": "api_reference",
            "product_area": "rate_limits",
            "url": "https://docs.logiflow.io/rate-limits",
            "last_updated": "2026-06-01",
        },
        "03_error_codes.md": {
            "source_name": "API Reference — Error Codes",
            "source_type": "api_reference",
            "product_area": "errors",
            "url": "https://docs.logiflow.io/error-codes",
            "last_updated": "2026-06-01",
        }

    }

    for d in documents:
        filename = d.metadata["source"].split("/")[-1]  # PyMuPDFLoader sets this automatically
        meta = SourceMetadata(**file_metadata[filename])
        d.metadata.update(meta.model_dump(mode = "json"))
    return documents

@timed
def doc_chunk(documents):
    """Split loaded documents into smaller overlapping chunks.

Uses the configured text splitter (e.g. RecursiveCharacterTextSplitter)
to break each Document into retrieval-sized pieces, preserving each
chunk's original metadata (source name, source type, product type) for 
later citation.

Args:
    documents (list[Document]): Raw documents.

Returns:
    list[Document]: Smaller chunked documents, ready for embedding and
        indexing into the vector store.
"""
    all_chunks = []
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on= [("#", "Title"), ("##", "Section")],
        strip_headers= False)
    for doc in documents:
        chunks = splitter.split_text(doc.page_content)
        for chunk in chunks:
            chunk.metadata.update(doc.metadata)
            if chunk.metadata['Title'] == 'Error Codes' and chunk.metadata['Section'] == 'Error Response Format':
                chunk.metadata['product_area'] = "errors"
            if chunk.metadata['Title'] == 'Error Codes' and chunk.metadata['Section'] == 'Shipment Errors':
                chunk.metadata['product_area'] = "shipments"
            if chunk.metadata['Title'] == 'Error Codes' and chunk.metadata['Section'] == 'Bulk Upload Errors':
                chunk.metadata['product_area'] = "shipments"
            if chunk.metadata['Title'] == 'Error Codes' and chunk.metadata['Section'] == 'Webhook Delivery Errors':
                chunk.metadata['product_area'] = "webhooks"

            chunk.metadata.pop("Title", None)
            chunk.metadata.pop("Section", None)
            all_chunks.append(chunk)
    return all_chunks

@timed
def vector_emb(all_chunks):
    """Embed document chunks and store them in a Chroma vector store.

Uses the configured embedding model (e.g. HuggingFaceEmbeddings) to
convert each chunk's text into a vector, then persists the chunks and
their vectors in ChromaDB for later similarity search / retrieval.

Args:
    chunks (list[Document]): Chunked documents.

Returns:
    Chroma: A Chroma vector store instance containing the embedded
        chunks, ready to be wrapped in a retriever.
"""
    vector_store = Chroma.from_documents(
        documents = all_chunks,
        embedding = emb,
        persist_directory = "chroma store",
        collection_metadata = {"hnsw:space" : "cosine"})
    return vector_store

if __name__ == "__main__":
    documents = load_data()
    all_chunks = doc_chunk(documents)
    vector_store = vector_emb(all_chunks)