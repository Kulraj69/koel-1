import streamlit as st
import chromadb
import os
from openai import AzureOpenAI
import uuid
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Kirloskar RAG Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load configuration from Streamlit secrets

CHROMADB_API_KEY = st.secrets["chromadb"]["api_key"]
CHROMADB_TENANT = st.secrets["chromadb"]["tenant"]
CHROMADB_DATABASE = st.secrets["chromadb"]["database"]
    
AZURE_ENDPOINT = st.secrets["azure_openai"]["endpoint"]
AZURE_DEPLOYMENT = st.secrets["azure_openai"]["deployment"]
AZURE_API_KEY = st.secrets["azure_openai"]["api_key"]
AZURE_API_VERSION = st.secrets["azure_openai"]["api_version"]


class RAGBot:
    def __init__(self):
        self.chroma_client = None
        self.azure_client = None
        self.collection = None
        self.initialize_clients()
    
    def initialize_clients(self):
        """Initialize ChromaDB and Azure OpenAI clients"""
        try:
            # Initialize ChromaDB client
            self.chroma_client = chromadb.CloudClient(
                api_key=CHROMADB_API_KEY,
                tenant=CHROMADB_TENANT,
                database=CHROMADB_DATABASE
            )
            
            # Initialize Azure OpenAI client
            self.azure_client = AzureOpenAI(
                azure_endpoint=AZURE_ENDPOINT,
                api_key=AZURE_API_KEY,
                api_version=AZURE_API_VERSION,
            )
            
            # List all collections to find existing ones
            collections = self.chroma_client.list_collections()
            
            # Connect to the collection with documents (fresh_start)
            collection_with_docs = None
            for col in collections:
                if col.count() > 0:
                    collection_with_docs = col
                    break
            
            if collection_with_docs:
                self.collection = collection_with_docs
            else:
                # Create new collection if none have documents
                self.collection = self.chroma_client.get_or_create_collection(
                    name="kirloskar_knowledge_base",
                    metadata={"description": "Kirloskar company knowledge base"}
                )
            return True
            
        except Exception as e:
            st.error(f"❌ Error initializing clients: {str(e)}")
            return False
    
    def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """Add documents to the vector database"""
        try:
            if not texts:
                return False
                
            # Generate unique IDs for documents
            ids = [str(uuid.uuid4()) for _ in texts]
            
            # Add default metadata if none provided
            if metadatas is None:
                metadatas = [{"source": "user_upload", "timestamp": datetime.now().isoformat()} for _ in texts]
            
            # Add documents to collection
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            return True
            
        except Exception as e:
            st.error(f"Error adding documents: {str(e)}")
            return False
    
    def query_documents(self, query: str, n_results: int = 5):
        """Query the vector database for relevant documents"""
        try:
            collection_count = self.collection.count()
            
            if collection_count == 0:
                return None
            
            # Perform the query - try different approaches for embedding compatibility
            try:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    include=['documents', 'metadatas', 'distances']
                )
            except Exception:
                # Fallback: search by getting all documents and filtering (simple text search)
                all_docs = self.collection.get(include=['documents', 'metadatas'])
                
                # Simple keyword matching
                query_lower = query.lower()
                matching_docs = []
                matching_metadatas = []
                
                for i, doc in enumerate(all_docs['documents']):
                    if any(word in doc.lower() for word in query_lower.split()):
                        matching_docs.append(doc)
                        matching_metadatas.append(all_docs['metadatas'][i] if all_docs['metadatas'] else {})
                        if len(matching_docs) >= n_results:
                            break
                
                # Format results to match ChromaDB query format
                results = {
                    'documents': [matching_docs],
                    'metadatas': [matching_metadatas],
                    'distances': [[0.5] * len(matching_docs)]  # Dummy distances
                }
            
            return results
            
        except Exception as e:
            st.error(f"Error querying documents: {str(e)}")
            return None
    
    def generate_response(self, query: str, context_docs: List[str]):
        """Generate response using Azure OpenAI with retrieved context"""
        try:
            # Prepare context from retrieved documents
            context = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(context_docs)])
            
            # Create system prompt with context
            system_prompt = f"""You are a helpful AI assistant for Kirloskar company. Use the following context documents to answer the user's question. If the answer cannot be found in the context, say so clearly.

Context Documents:
{context}

Please provide accurate, helpful responses based on the context provided."""

            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
            
            # Generate completion
            completion = self.azure_client.chat.completions.create(
                model=AZURE_DEPLOYMENT,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I encountered an error while generating a response."
    
    def get_collection_stats(self):
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {"document_count": count}
        except Exception as e:
            return {"document_count": 0}

def main():
    st.title("🤖 Kirloskar RAG Bot")
    st.markdown("---")
    
    # Initialize RAG bot
    if 'rag_bot' not in st.session_state:
        st.session_state.rag_bot = RAGBot()
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for bot info
    with st.sidebar:
        st.header("📊 Knowledge Base Info")
        
        # Collection stats
        stats = st.session_state.rag_bot.get_collection_stats()
        st.metric("Documents in Database", stats['document_count'])
        
        st.markdown("---")
        
        st.subheader("💡 About this Bot")
        st.write("This RAG bot is connected to your Kirloskar knowledge base and can answer questions about:")
        st.write("• Company information")
        st.write("• Products and services")
        st.write("• Technical documentation")
        st.write("• Business operations")
        
        st.markdown("---")
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main chat interface
    st.header("💬 Chat with your Knowledge Base")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📄 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.text(f"Source {i}: {source[:200]}...")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your documents..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base and generating response..."):
                # Query vector database
                query_results = st.session_state.rag_bot.query_documents(prompt, n_results=3)
                
                if query_results and query_results['documents'][0]:
                    # Get relevant documents
                    relevant_docs = query_results['documents'][0]
                    
                    # Generate response
                    response = st.session_state.rag_bot.generate_response(prompt, relevant_docs)
                    
                    # Display response
                    st.markdown(response)
                    
                    # Add to chat history with sources
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                        "sources": relevant_docs
                    })
                    
                    # Show sources
                    with st.expander("📄 View Sources"):
                        for i, doc in enumerate(relevant_docs, 1):
                            st.text(f"Source {i}: {doc[:200]}...")
                else:
                    response = "I couldn't find any relevant documents in the knowledge base. Please add some documents first."
                    st.markdown(response)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })

if __name__ == "__main__":
    main()
