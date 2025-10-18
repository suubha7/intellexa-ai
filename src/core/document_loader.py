from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader, TextLoader, Docx2txtLoader
import os

class Document_loader:
    def __init__(self):
        self.file_formats = {
                            '.pdf': PyPDFLoader,
                            '.txt': TextLoader,
                            '.docx': Docx2txtLoader
                        }

    def load_company_kb(self):
        self.folder_path = r"C:\Intellexa AI\data\company_kb"
        all_docs = []
        for ext, loader_class in self.file_formats.items():
            loader = DirectoryLoader(
                path=self.folder_path,
                glob=f"**/*{ext}",
                loader_cls=loader_class
            )
            docs = loader.load()
            for d in docs:
                d.metadata["page_label"] = d.metadata.get("page_label", 1)
            all_docs.extend(docs)

        return all_docs

    def load_user_file(self, user_file_path: str):
        file_ext = os.path.splitext(user_file_path)[1].lower()
        
        if file_ext == '.pdf':
            loader = PyPDFLoader(user_file_path)
        elif file_ext == '.docx':
            loader = Docx2txtLoader(user_file_path)
        elif file_ext == '.txt':
            loader = TextLoader(user_file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        docs = loader.load()
        for d in docs:
            d.metadata["page_label"] = d.metadata.get("page_label", 1)
        return docs