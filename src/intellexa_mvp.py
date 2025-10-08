from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
import os


print(f"{'-'*45} 🚀 Intellexa AI : Basic RAG MVP {'-'*45}")

def pdf_loader(file_path: str):
    """Load PDF file from the path."""

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print("Document loaded successfully!")
    return documents
    

def doc_chunker(documents):
    """Convert documents into chunks."""
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        
        return chunks
    except Exception as e:
        print(f"Failed to chunk document: {e}")
        return None

def vectorstore(chunks, metadata=None):
    """Store the chunks into vectorstore after converting to embeddings."""

    try:
        embedding = VertexAIEmbeddings(model_name="text-embedding-005")
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory="./chroma_db"
        )
        print("Vectorstore created successfully!")
        return vectordb
    except Exception as e:
        print(f"Failed to create vectorstore: {e}")
        return None
    
def retrieve_context(query: str, vectorstore):
    """Search relevant chunks by the query."""
    try:
        context = vectorstore.similarity_search(query, k=3)
        
        return context
    except Exception as e:
        print(f"Failed to retrieve context: {e}")
        return []

def qa_chain(query, context):
    """Answer the question based on retrieved context."""

    try:
        # Combine context for LLM
        context_text = "\n\n".join([doc.page_content for doc in context])
        
        # Get sources and pages
        sources = []
        for doc in context:
            source = os.path.basename(doc.metadata.get('source', 'Unknown'))
            page = doc.metadata.get('page', 0) + 1
            sources.append(f"{source} (Page {page})")
        
        
        unique_sources = list(set(sources))
        
        template = """Use the following context to answer the question. 
                    If you don't know the answer, just say Sorry you don't know.

                    Context: {context}
                    Question: {query}
                    Answer:"""
        prompt = PromptTemplate(
            template=template,
            input_variables=['context','query']
        )
        
        llm = init_chat_model(model="gemini-2.5-flash-lite", model_provider="google_vertexai")
        
        chain = prompt | llm
        response = chain.invoke({
            'context': context_text,
            'query': query
        })
        
        return response.content, unique_sources
    except Exception as e:
        print(f"Failed to generate answer: {e}")
        return "Sorry, something went wrong.", []




if __name__ == "__main__":
    # Load documents 
    documents = pdf_loader(r"src\Insurance_Policy.pdf")
    if not documents:
        print("Failed to load documents. Exiting.")
        exit()

    # Chunk the documents 
    chunks = doc_chunker(documents)
    if not chunks:
        print("Failed to chunk documents. Exiting.")
        exit()

    # Create vectorstore
    vectordb = vectorstore(chunks)
    if not vectordb:
        print("Failed to create vectorstore. Exiting.")
        exit()

    print("\n\n🧠 Intellexa AI is ready! Ask your questions:\n")

    while True:
        query = input("✍️ Enter your question or exit: ")
        if query.lower() == 'exit':
            print('...........Thanks You for using Intellexa AI...........')
            break

        context_docs = retrieve_context(query, vectordb)
        if not context_docs:
            print("No relevant context found.")
            continue
        answer, sources = qa_chain(query,context_docs)

        print(f'-'*150)
        print('💡 Answer 💡')
        print(f'-'*150)

        print(f"{answer}")
        if sources:
            print(f"\nSources: {', '.join(sources)}")
        print(f"{'-'*150}\n")