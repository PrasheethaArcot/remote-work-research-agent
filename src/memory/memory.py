import uuid
from typing import List
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_community.embeddings import HuggingFaceEmbeddings

# Create in-memory vector store
recall_vector_store = InMemoryVectorStore(
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
)


def get_user_id(config: RunnableConfig) -> str:
    return config["configurable"].get("user_id", "default")

@tool
def save_recall_memory(memory: str, config: RunnableConfig) -> str:
    """Save a memory string to the recall vector store for a given user."""
    user_id = get_user_id(config)
    doc = Document(page_content=memory, id=str(uuid.uuid4()), metadata={"user_id": user_id})
    recall_vector_store.add_documents([doc])
    return memory

@tool
def search_recall_memories(query: str, config: RunnableConfig) -> List[str]:
    """Search recall memory for a given query and user ID."""
    user_id = get_user_id(config)
    def _filter(doc): return doc.metadata.get("user_id") == user_id
    docs = recall_vector_store.similarity_search(query, k=3, filter=_filter)
    return [d.page_content for d in docs]
