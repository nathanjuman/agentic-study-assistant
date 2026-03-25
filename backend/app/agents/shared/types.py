"""
Shared data shapes that the text RAG flow will use.

Keeps later ingestion, retrieval, and RAG orchestration code
working with stable typed objects instead of loose dictionaries.

"""
from dataclasses import field
from pydantic.dataclasses import dataclass


@dataclass
class Citation:
    """User-facing citation payload derived from retrieved chunks."""
    file_id: str
    filename: str
    page_number: int | None
    snippet: str
    score: float | None = None


@dataclass
class RetrievedChunk:
    """Normalized retrieval result shared across retrieval and answer generation."""
    chunk_id: str
    file_id: str
    filename: str
    text: str
    chunk_index: int
    page_number: int | None
    score: float | None = None
    metadata: dict[str, str | int | float | None] = field(default_factory=dict)


@dataclass
class RetrievalContext:
    """Full retrieval bundle passed into the RAG answering layer."""
    query: str
    chunks: list[RetrievedChunk]
    citations: list[Citation]
