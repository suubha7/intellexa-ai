from src import config
from langchain.chat_models import init_chat_model
from langchain.chains.summarize import load_summarize_chain


class Summarizer:
    def __init__(self):
         self.llm = init_chat_model(
            model="gemini-2.5-flash-lite", 
            model_provider="google_vertexai"
            )

    def summarize(self,chunks):
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        return chain.run(chunks)