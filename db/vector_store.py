from langchain_community.vectorstores import Chroma
from langchain_classic.embeddings import SentenceTransformerEmbeddings
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vec_store = Chroma(
    embedding_function = embedding_function,
    persist_directory = "chroma_db",
    collection_name="task_vectors",
    collection_metadata={"hnsw:space": "cosine"}
)
