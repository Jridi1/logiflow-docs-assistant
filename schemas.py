from pydantic import BaseModel, Field
from typing import Literal

class SourceCitation(BaseModel):
    source_name: str = Field(..., description="Human-readable document title, e.g. 'API Reference — Rate Limits'.")
    product_area: str = Field(..., description="Topic this chunk belongs to.")
    url: str = Field(..., description="Link to the source document.")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="The generated answer, grounded in the provided context.")
    is_answerable: bool = Field(..., description="False if the context did not contain enough information to answer.")
    confidence: Literal["high", "medium", "low"] = Field(..., description="Model's confidence in the answer.")
    sources: list[SourceCitation] = Field(default_factory=list, description="Documents used to generate the answer.")

class QueryRequest(BaseModel):
    question: str
    session_id: str