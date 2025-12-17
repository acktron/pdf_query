from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf_utils import extract_text_from_pdf, build_context_for_llm
from llm_client import answer_question_from_context

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/debug-query-pdf")
async def debug_query_pdf():
    return {"status": "ok", "detail": "query-pdf backend is running"}

@app.post("/query-pdf")
async def query_pdf(file: UploadFile, question: str = Form(...)):
    """
    Process PDF upload and answer user's question using Ollama.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")
    
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        pdf_bytes = await file.read()
        text = extract_text_from_pdf(pdf_bytes)
        context, truncated = build_context_for_llm(text)
        
        answer = answer_question_from_context(question.strip(), context)
        
        response_data = {
            "answer": answer,
            "context_truncated": truncated,
            "context_length": len(context)
        }
        
        return JSONResponse(content=response_data)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
async def serve_frontend():
    """Serve frontend HTML"""
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
