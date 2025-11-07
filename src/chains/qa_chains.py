from src.utils import get_llm
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

class QAchain:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = self.create_prompt()

    def create_prompt(self):
        template = """Use the following context to answer the question. 
        If you don't know the answer, just politely say you don't know. Be helpful and accurate.
        your name intellexa ai

        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=['context', 'question']
        )

    def create_qa_chain(self, retriever):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": self.prompt},
            return_source_documents=True
        ) 