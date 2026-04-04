from db.vector_store import vec_store

print(vec_store.get(include=["embeddings", "documents", "metadatas"]))