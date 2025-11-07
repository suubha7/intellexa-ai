from src.utils import get_llm
from langchain.chains.summarize import load_summarize_chain


class Summarizer:
    def __init__(self):
         self.llm = get_llm()

    def summarize(self,chunks):
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        return chain.run(chunks)