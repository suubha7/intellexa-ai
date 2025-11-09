from src.utils import get_llm
from langchain.chains.summarize import load_summarize_chain


class Summarizer:
    def __init__(self):
         self.llm = get_llm()

    def summarize(self,chunks):
        chain = load_summarize_chain(llm=self.llm, chain_type="map_reduce",verbose=True)
        result = chain.invoke({'input_documents':chunks})

        return result['output_text']