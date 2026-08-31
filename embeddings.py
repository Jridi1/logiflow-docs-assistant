from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )