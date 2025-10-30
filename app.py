from src.core.document_loader import Document_loader
from src.core.text_splitter import TextSplitter
from src.vectore_store.chromadb_manager import Vector_manager
from src.chains.qa_chains import QAchain
from src.chains.summarizer import Summarizer
import streamlit as st
import hashlib
import os

st.set_page_config("Intellexa AI", page_icon="🧠", layout="wide")

# avoid reprocessing
def get_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    
def get_processed_document(file_path= None):
    loader = Document_loader()
    if file_path == None:
        doc = loader.load_company_kb()
    else:
        doc = loader.load_user_file(file_path)
    splitter = TextSplitter()
    chunks = splitter.document_chunker(doc)
    return chunks

# Answer, source extractor
def get_answer_source(response, source_type="user"):
    ans = response['result']
    source = []
    check = set()

    for doc in response['source_documents']:
        if source_type == "user":
            file_name = st.session_state.get("original_filename") or os.path.basename(doc.metadata['source'])
        else:
            file_name = os.path.basename(doc.metadata['source'])

        page = doc.metadata.get('page_label') or doc.metadata.get('page', 0) + 1
        src = f'File_name: {file_name} || Page: {page}'

        if src not in check:
            source.append(src)
            check.add(src)

    return ans, source

# Sidebar
st.sidebar.title("🧠 Intellexa AI")

# Tabs
selected_tab = st.radio("Navigate", ['PDF Q&A', 'Company Knowledge Base', 'Summarizer'], horizontal=True, label_visibility="collapsed")

# Session state init
st.session_state.setdefault("pdf_chat_history", [])
st.session_state.setdefault("company_chat_history", [])

# PDF Q&A TAB
if selected_tab == "PDF Q&A":
    st.subheader("Ask Your Document")

    uploaded_file = st.file_uploader("Upload your PDF and start asking questions about it.", type=['pdf', 'txt', 'docx'], key="qa")

    if uploaded_file:
        with st.spinner("Uploading and indexing..."):
            os.makedirs("data/user_documents", exist_ok=True)
            file_extension = os.path.splitext(uploaded_file.name)[1]
            file_path = f"data/user_documents/current_user_file{file_extension}"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state.original_filename = uploaded_file.name
            file_hash = get_file_hash(file_path)

            if st.session_state.get("last_file_hash") != file_hash:
                chunks = get_processed_document(file_path)

                vector_manager = Vector_manager()
                faiss_db = vector_manager.create_faiss_vector_store(chunks)
                st.session_state.user_vectordb = faiss_db.as_retriever(search_kwargs={"k": 3})
                st.session_state.last_file_hash = file_hash
                st.session_state.pdf_chat_history = []

            st.success("File uploaded and indexed successfully!")

    if "user_vectordb" in st.session_state:
        qa = QAchain()
        user_input = st.text_input("question", key="user_key")
        qa_chain = qa.create_qa_chain(st.session_state.user_vectordb)

        if st.button('send', key="pdf_send") and user_input:
            with st.spinner("Thinking..."):
                try:
                    response = qa_chain.invoke({'query': user_input})
                    answer, source = get_answer_source(response)
                    st.text_area("Answer:", value=answer, height=200, disabled=True)
                    st.text_area("Sources:", value="\n".join(source), height=50, disabled=True)
                    st.session_state.pdf_chat_history.append({
                        "question": user_input,
                        "answer": answer,
                        "sources": source
                    })
                except Exception as e:
                    st.error(f"Error during QA: {str(e)}")
    else:
        st.info("Please upload a file first to ask questions.")

# Company Knowledge Base TAB
elif selected_tab == "Company Knowledge Base":
    st.subheader("Company Knowledge Base")

    if "company_vectordb" not in st.session_state:
        with st.spinner("Loading company knowledge base..."):
            chunks = get_processed_document()

            vector_manager = Vector_manager()
            chroma_db = vector_manager.create_chroma_vector_store(chunks, persist_directory="./company_chroma_db")
            st.session_state.company_vectordb = chroma_db.as_retriever(search_kwargs={"k": 3})

    st.success("Company knowledge base ready for Q&A!")
    user_input = st.text_input("question", key="user_key2")
    qa = QAchain()
    qa_chain = qa.create_qa_chain(st.session_state.company_vectordb)

    if st.button('send', key="company_send") and user_input:
        with st.spinner("Thinking..."):
            try:
                response = qa_chain.invoke({'query': user_input})
                answer, source = get_answer_source(response ,source_type="company")
                st.text_area("Answer:", value=answer, height=200, disabled=True)
                st.text_area("Sources:", value="\n".join(source), height=50, disabled=True)
                st.session_state.company_chat_history.append({
                    "question": user_input,
                    "answer": answer,
                    "sources": source
                })
            except Exception as e:
                st.error(f"Error during QA: {str(e)}")

# Summarizer TAB
elif selected_tab == "Summarizer":
    st.subheader('Summarize It Fast')

    uploaded_file = st.file_uploader("Upload your PDF and start asking questions about it.", type=['pdf', 'txt', 'docx'], key="summarize")
    if uploaded_file:
        with st.spinner("File Summarizing .........."):
            os.makedirs("temp_files", exist_ok=True)
            file_extension = os.path.splitext(uploaded_file.name)[1]
            file_path = f"temp_files/current_user_file{file_extension}"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state.original_filename = uploaded_file.name
            file_hash = get_file_hash(file_path)

            summarized_response = ""
            if st.session_state.get("last_summarizer_hash") != file_hash:
                chunks = get_processed_document(file_path)

                summarizer = Summarizer()
                summarized_response = summarizer.summarize(chunks)
                st.session_state.last_summarizer_hash = file_hash
            st.text_area("Answer:", value=summarized_response, height=300, disabled=True)

# Sidebar Chat History
if selected_tab == "PDF Q&A":
    st.sidebar.subheader("PDF Chat History")
    if st.session_state.pdf_chat_history:
        for chat in st.session_state.pdf_chat_history:
            st.sidebar.write(f"**Q:** {chat['question']}")
            st.sidebar.write(f"**A:** {chat['answer'][:100]}...")
            st.sidebar.write("---")
    else:
        st.sidebar.info("No chat history yet")

elif selected_tab == "Company Knowledge Base":
    st.sidebar.subheader("Company KB History")
    if st.session_state.company_chat_history:
        for chat in st.session_state.company_chat_history:
            st.sidebar.write(f"**Q:** {chat['question']}")
            st.sidebar.write(f"**A:** {chat['answer'][:100]}...")
            st.sidebar.write("---")
    else:
        st.sidebar.info("No chat history yet")

elif selected_tab == "Summarizer":
    st.sidebar.subheader("Summarizer")
    st.sidebar.info("Upload your documents[pdf, txt, docx] and get summarized response")
