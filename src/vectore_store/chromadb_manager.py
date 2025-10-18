from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma

class Vector_manager:
    def __init__(self):
        self.embedding = VertexAIEmbeddings(model_name="text-embedding-005")
    
    def create_vector_store(self,chunks , persist_directory: str):
        self.persist_directory = persist_directory

        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding,
            persist_directory=persist_directory
        )

        return vectordb
    
    def load_vector_store(self, persist_directory: str):
    
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding
        )
        return vectordb