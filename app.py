from src.core.document_loader import Document_loader
from src.core.text_splitter import Text_splitter
from src.vectore_store.chromadb_manager import Vector_manager
from src.chains.qa_chains import QAchain
import streamlit as st
import os

st.set_page_config("Intellexa AI",page_icon="🧠",layout="wide")

# all in one
def vectore_db(path,db_folder ="./company_chroma_db"):
    loader = Document_loader()
    if path is None:
        doc = loader.load_company_kb()
    else:
        doc = loader.load_user_file(path)

    splitter = Text_splitter()
    chunks = splitter.document_chunker(doc)
    vector_manager = Vector_manager()
    chroma_db = vector_manager.create_vector_store(chunks,db_folder)
    return chroma_db


# retrieve answer and source at one place
def get_answer_source(responce):
    ans = responce['result']
    source = []
    check = set()
    for doc in responce['source_documents']:
        if 'original_filename' in st.session_state:
            file_name = st.session_state.original_filename
        else:
            file_name = os.path.basename(doc.metadata['source'])
        page = doc.metadata.get('page_label') or doc.metadata.get('page_label',0)+1
        src = f'File_name: {file_name} || Page: {page}'
        if src not in check:
            source.append(src)
            check.add(src)     
    return ans, source

# Starting UI from title
st.title("Intellexa AI - Enterprise Knowledge Platform")

pdf_qa, company_kb = st.tabs(["PDF QA",'Company KB'])


# User QA interface
with pdf_qa:
    st.subheader("PDF Question Ans")
      
    uploaded_file = st.file_uploader("Upload your PDF and start asking questions about it.",type=['pdf','txt','docx'])
    if uploaded_file:
        with st.spinner("File uploading .........."):
            # Create folder if doesn't exist
            os.makedirs("data/user_documents", exist_ok=True)
            
            file_extension = os.path.splitext(uploaded_file.name)[1]
            # Save file
            file_path = f"data/user_documents/current_user_file{file_extension}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.original_filename = uploaded_file.name

            if "user_vectordb" not in st.session_state:
                    user_db = vectore_db(path=file_path,db_folder="./user_chroma_db")
                    st.session_state.user_vectordb = user_db.as_retriever(search_kwargs={"k": 3})
            st.success("File uploaded sucussesfully!")

    
    
  
    if "user_vectordb" in st.session_state:
        qa = QAchain()
        user_input = st.text_input("question",key="user_key")
        qa_chain = qa.create_qa_chain(st.session_state.user_vectordb)
        
        if st.button('send', key="pdf_send") and user_input:
            with st.spinner("Thinking..."):
                response = qa_chain.invoke({'query': user_input})
            
            answer, source = get_answer_source(response)
            st.markdown("Answer:")
            st.write(answer)
            st.markdown("Source:")
            st.write(source)
    else:
        st.info("📁 Please upload a file first to ask questions")
        




# Company KB interface
with company_kb:
    st.subheader("Company KB")

    if "company_vectordb" not in st.session_state:
        with st.spinner("Loading company knowledge base..."):
            chroma_db_kb = vectore_db(path=None)
            st.session_state.company_vectordb = chroma_db_kb.as_retriever(search_kwargs={"k": 3})
    st.success("Company knowledge base ready for Q&A!")

    st.markdown("---")
    user_input = st.text_input("question",key="user_key2")

    qa = QAchain()
    qa_chain = qa.create_qa_chain(st.session_state.company_vectordb)
    

    if st.button('send', key="company_send") and user_input:
                
        with st.spinner("Thinking..."):
            response = qa_chain.invoke({'query': user_input})
        
        answer, source = get_answer_source(response)
        st.markdown("Answer:")
        st.write(answer)
        st.markdown("Source:")
        st.write(source)
                

    