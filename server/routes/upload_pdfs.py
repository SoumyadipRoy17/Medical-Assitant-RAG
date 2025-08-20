from fastapi import APIRouter, File, UploadFile
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger

router=APIRouter()

@router.post("/upload_pdfs")
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info("Received uploaded files")
        load_vectorstore(files)
        logger.info("Document added to vector store")
        return {"message": "PDFs uploaded successfully and vector_store updated"}
    except:
        logger.exception("Error uploading PDFs")
        return JSONResponse(status_code=500, content={"message": "Error uploading PDFs"})