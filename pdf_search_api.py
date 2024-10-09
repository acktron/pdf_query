from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from PyPDF2 import PdfReader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from typing_extensions import Concatenate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain import HuggingFaceHub
from huggingface_hub import login
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from fastapi.middleware.cors import CORSMiddleware
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "api"
import io

app = FastAPI()

# Step 2: Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; you can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
@app.post("/search_pdf/")
async def search_pdf(file: UploadFile, query: str = Form(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    try:
        # Read the PDF file
        pdfreader = PdfReader(io.BytesIO(await file.read()))
        raw_text = ''
        for i, page in enumerate(pdfreader.pages):
            content = page.extract_text()
            if content:
                raw_text += content
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len
        )
        texts = text_splitter.split_text(raw_text)
        embeddings = HuggingFaceEmbeddings()
        document_search = FAISS.from_texts(texts[:80], embeddings)
        repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"
        llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.5, max_length= 512, token = "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")
        chain = load_qa_chain(llm, chain_type="stuff")
        from langchain import PromptTemplate, LLMChain

        # Define the user's query
        #query = "How many types of mindsets are there?"

        # Perform a similarity search to find relevant documents
        docs = document_search.similarity_search(query)

        # Create a prompt template for generating responses
        template = """Given the following conversation, relevant context, and a follow up question, reply with an answer to the current question the user is asking. 
        Return only your response to the question given the above information following the users instructions as needed.
        Context:
        {docs}

        Question:
        {query}
        """

        # Initialize the prompt template with specified input variables
        prompt = PromptTemplate(template=template, input_variables=["docs", "query"])

        # Set up the LLMChain with the language model and prompt
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        # Execute the chain and get the response
        response = llm_chain.run({'docs': docs, 'query': query})

        # Print the relevant documents and the generated response
        #print(docs)

        if docs != '':
            return JSONResponse(content={
                "message": "Query found in the PDF!",
                "Answer": response
            })
        else:
            return JSONResponse(content={"message": "Query not found in the PDF."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
