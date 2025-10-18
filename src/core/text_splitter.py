from langchain_text_splitters import RecursiveCharacterTextSplitter


class Text_splitter:
    def __init__(self):
        pass

    def document_chunker(self,documents: list) -> list:
        splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)

        chunks = splitter.split_documents(documents)
    
        return chunks