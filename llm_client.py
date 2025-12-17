import os
import requests
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def answer_question_from_context(question: str, context: str) -> str:
    """
    Use Ollama to answer a question based on provided context.
    
    Args:
        question: User's question
        context: Extracted text from PDF
        
    Returns:
        Answer string from Ollama
        
    Raises:
        ValueError: If Ollama API call fails
    """
    ollama_url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    model_name = os.getenv("OLLAMA_MODEL", "tinyllama")
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len
    )
    texts = text_splitter.split_text(context)
    
    embeddings = HuggingFaceEmbeddings()
    document_search = FAISS.from_texts(texts[:80], embeddings)
    
    docs = document_search.similarity_search(question)
    docs_str = "\n".join([doc.page_content for doc in docs])
    
    prompt = f"Context: {docs_str}\n\nQuestion: {question}\n\nAnswer:"
    
    api_url = f"{ollama_url}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if "response" in result:
            return result["response"].strip()
        else:
            raise ValueError("Unexpected response format from Ollama")
            
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error calling Ollama API: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing Ollama response: {str(e)}")
