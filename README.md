# 🚀 Intellexa AI - Enterprise 

## One-liner
"Intellexa AI helps answer questions from company or user documents using RAG technology."

## Overview
Intellexa AI is a Retrieval-Augmented Generation (RAG) based system that allows users to ask questions directly from PDF documents.  
It uses LangChain and Google Vertex AI to split, embed, and search documents efficiently, providing accurate answers with source references.

## Problem Statement
Many companies have important information spread across many PDF documents.
Finding the right information takes a lot of time and effort. This slows down work and decision-making.

## Tools and Technologies
- **Python** - with LangChain framework
- **ChromaDB** - vector database with persistence
- **PyPDFLoader** - Load PDF documents
- **RecursiveCharacterTextSplitter** - Split documents into manageable chunks
- **VertexAIEmbeddings** - Convert text into embeddings for semantic search
- **Chroma Vector Database** - vector database with persistence
- **Gemini LLM** - Generate answers from retrieved context
- **Professional error handling** and modular design

## Methods & Key Insights
1. **PDF Loading**: Extracts text from uploaded PDFs.  
2. **Text Chunking**: Splits long documents into smaller chunks for better semantic search.  
3. **Embeddings & Vectorstore**: Converts chunks into embeddings and stores them in Chroma for fast retrieval.  
4. **Context Retrieval**: Searches for the most relevant chunks based on user queries.  
5. **Answer Generation**: Uses Gemini LLM to generate answers from retrieved context.  
6. **Sources Tracking**: Displays the source document and page for transparency.  

**Key Insight:** Combining RAG with vector search ensures accurate, context-aware answers from large documents.

## Output / Model
- Users enter a question in the terminal.
- System retrieves the most relevant chunks from the PDF(s) and generates a concise answer.
- Each answer includes **source references** with document name and page numbers.

**Example:**
--------------------------------------------- 🚀 Intellexa AI : Basic RAG MVP ---------------------------------------------

Document loaded successfully!

Vectorstore created successfully!


🧠 Intellexa AI is ready! Ask your questions:

✍️ Enter your question or exit: describe me about life insurance policy

------------------------------------------------------------------------------------------------------------------------------
💡 Answer 💡

The life insurance policy is a Term Life Insurance policy from SecureLife Assurance Co., with policy number LIP-2025-112. The policyholder is Jane Smith, and the coverage period is from 01-Feb-2025 to 31-Jan-2045.

The policy has the following features:
*   **Exclusions:** Injuries from hazardous sports, self-harm or substance abuse, and war, riots, or nuclear risks.
*   **Premium:** USD 500 annually, with a 15-day grace period for payment.
*   **Claims:**
    *   Notify the insurer within 48 hours.
    *   Submit hospital bills, discharge summary, and ID proof.
    *   Claim settlement within 30 days.

Sources: Insurance_Policy.pdf (Page 1)

----------------------------------------------------------------------------------------------------------------------------------

✍️ Enter your question or exit: how to claim travel insurance policy

----------------------------------------------------------------------------------------------------------------------------------
💡 Answer 💡

To claim travel insurance policy, you need to:
*   Report the incident to the insurer or international helpline within 24 hours.
*   Submit medical bills, travel documents, and boarding passes.
*   The claim will be settled within 30 working days.

Sources: Insurance_Policy.pdf (Page 2)

---------------------------------------------------------------------------------------------------------------------------------
✍️ Enter your question or exit: exit

...........Thanks You for using Intellexa AI...........

## How to run
1. Clone repository
```bash
git clone https://github.com//intellexa-ai.git
cd intellexa-ai
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Set up Google Cloud credentials
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```
4. Place your PDF in the project folder (Sample.pdf as an example).

```bash
python .\src\intellexa-mvp.py
```
5. Ask questions in the terminal. Type exit to quit.

## Result & Conclusion
Intellexa AI successfully answers questions from PDFs with relevant context and source references.
It demonstrates the power of combining RAG with vector embeddings for document-based Q&A.
Conclusion: Enterprises can save significant time and improve decision-making by using AI to extract insights from documents spread across different locations.

## Future Work
- Phase 2: Web interface & multi-document support
- Phase 3: Research features & citations  
- Phase 4: Enterprise deployment with user auth

## Author
**Subham Maharana**
A fresher exploring AI, LangChain, and RAG systems. Built this project as part of learning enterprise AI applications and creating practical solutions for real-world document search challenges.