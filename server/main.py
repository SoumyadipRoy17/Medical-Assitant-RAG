from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exception_middleware
from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_router

app = FastAPI(title="Medical Assistant API", version="1.0.0",description="API for AI Medical Assistant application")

#CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE
    allow_headers=["*"],  # Allows all headers
)

#middleware exception handlers
app.middleware("http")(catch_exception_middleware)
#router



#upload pdf
app.include_router(upload_router)
#asking query
app.include_router(ask_router)
