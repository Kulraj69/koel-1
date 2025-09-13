# Kirloskar RAG Bot

A Retrieval-Augmented Generation (RAG) chatbot built with Streamlit, ChromaDB, and Azure OpenAI for the Kirloskar company knowledge base.

## Features

- 🤖 **Interactive Chat Interface**: Chat with your documents using natural language
- 📚 **Document Management**: Upload and manage documents in your knowledge base
- 🔍 **Semantic Search**: Find relevant information using vector similarity search
- 📄 **Source Attribution**: View the source documents used to generate responses
- 📊 **Real-time Stats**: Monitor the number of documents in your knowledge base

## Setup

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI API access
- ChromaDB Cloud account

### Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

The application is pre-configured with your ChromaDB and Azure OpenAI credentials:

- **ChromaDB**: Connected to your Kirloskar database
- **Azure OpenAI**: Using GPT-4o model deployment

## Usage

### Starting the Application

Run the Streamlit app:
```bash
streamlit run streamlit_ragbot.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Adding Documents

1. Use the sidebar to add documents to your knowledge base
2. You can either:
   - Paste text directly into the text area
   - Upload a `.txt` file
3. Click "➕ Add to Knowledge Base" to store the documents

### Chatting with Your Knowledge Base

1. Type your question in the chat input at the bottom
2. The bot will:
   - Search for relevant documents in your knowledge base
   - Generate a response using Azure OpenAI
   - Show the source documents used for the response

### Features

- **Document Upload**: Add text documents to your knowledge base
- **Semantic Search**: Find relevant information using vector embeddings
- **Source Attribution**: See which documents were used to generate each response
- **Chat History**: View your conversation history
- **Collection Stats**: Monitor the size of your knowledge base

## Architecture

- **Frontend**: Streamlit for the web interface
- **Vector Database**: ChromaDB Cloud for document storage and retrieval
- **LLM**: Azure OpenAI GPT-4o for response generation
- **Embeddings**: ChromaDB handles automatic embedding generation

## Troubleshooting

If you encounter any issues:

1. **Connection Errors**: Check your internet connection and API credentials
2. **Document Upload Errors**: Ensure your text files are UTF-8 encoded
3. **Response Generation Errors**: Verify your Azure OpenAI deployment is active

## Support

For questions or issues, please check:
- ChromaDB documentation: https://docs.trychroma.com/
- Azure OpenAI documentation: https://docs.microsoft.com/en-us/azure/cognitive-services/openai/
- Streamlit documentation: https://docs.streamlit.io/
