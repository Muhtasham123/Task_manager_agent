from db.vector_store import vec_store

all_ids = vec_store.get()["ids"]

vec_store.delete(ids = all_ids)
print(vec_store.get(include=["embeddings", "documents", "metadatas"]))