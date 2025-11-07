import os
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud.json"


def get_embadding_model():
    """Initialize the embadding model"""
    embedding = VertexAIEmbeddings(model_name="text-embedding-005")

    return embedding

def get_llm():
    """Initialize the chat model"""
    llm = init_chat_model(
            model="gemini-2.5-flash-lite", 
            model_provider="google_vertexai"
            )
    
    return llm

    