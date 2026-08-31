from langchain_core.prompts import ChatPromptTemplate

from retriever import retriever
from llm import build_llm
from schemas import QueryResponse, SourceCitation  # wherever you put the models above
from memory import get_history, add_to_history

from schemas import QueryResponse



prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a support assistant that answers questions using only the provided context. "
     "Never guess or use outside knowledge. If the context doesn't contain the answer, "
     "set is_answerable to false and explain briefly that this isn't covered in the documentation. "
     "Always cite which parts of the context you used."
     "If there's conversation history, use it to understand follow-up questions."),
    ("human", "Previous conversation:\n{history}\n\nContext:\n{context}\n\nQuestion: {question}"),
])



def format_docs(docs_and_scores: str):
    return "\n\n".join(doc.page_content for doc, score in docs_and_scores)
def build_sources(docs_and_scores):
    seen = set()
    sources = []
    for doc, score in docs_and_scores:
        name = doc.metadata["source_name"]
        if name in seen:
            continue
        seen.add(name)
        sources.append(SourceCitation(
            source_name=name,
            product_area=doc.metadata["product_area"],
            url=doc.metadata["url"],
        ))
    return sources

def ask(question: str, session_id: str) -> QueryResponse:
    history = get_history(session_id)
    history_text = "\n".join(f"Q: {h['question']}\nA: {h['answer']}" for h in history)

    docs_and_scores = retriever(question)

    if not docs_and_scores:
        return QueryResponse(
            answer="I don't have information about that in the documentation.",
            is_answerable=False,
            confidence="low",
            sources=[],
        )

    context = format_docs(docs_and_scores)

    model = build_llm()
    structured_model = model.with_structured_output(QueryResponse)

    chain = prompt | structured_model

    llm_response = chain.invoke({
        "context": context, 
        "question": question,
        "history": history_text
        })

    sources = build_sources(docs_and_scores)

    response = QueryResponse(
        answer=llm_response.answer, 
        is_answerable=llm_response.is_answerable, 
        confidence=llm_response.confidence, 
        sources=sources
        )
    add_to_history(session_id, question, response.answer)
    return response
    

