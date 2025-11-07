from src.utils import get_embadding_model
from langchain_community.vectorstores import FAISS, Chroma

class Vector_manager:
    def __init__(self):
        self.embedding = get_embadding_model()

    # FAISS for user-uploaded files (in-memory)
    def create_faiss_vector_store(self, chunks):
        return FAISS.from_documents(documents=chunks, embedding=self.embedding)

    # Chroma for company KB (persistent)
    def create_chroma_vector_store(self, chunks, persist_directory):
        return Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding,
            persist_directory=persist_directory
        )

    def load_chroma_vector_store(self, persist_directory):
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding
        )