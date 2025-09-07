import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone,ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medical-assistant-index"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#initialize pinecone instance

pc = Pinecone(
    api_key=PINECONE_API_KEY)

sc=ServerlessSpec(
        cloud="aws",
        region="us-east-1",
    )

existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,  # Dimension for Google Generative AI embeddings
        metric="cosine",
        spec=sc
    )
    print(f"Index {PINECONE_INDEX_NAME} created.")
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        print("Waiting for index to be ready...")
        time.sleep(1)
index = pc.Index(PINECONE_INDEX_NAME)

# load , split embed and upsert pdf docs content

# def load_vectorstore(uploaded_files):
#     """
#     Load a PDF file, split it into chunks, embed the chunks, and upsert them into Pinecone.
    
#     Args:
#         pdf_file (Path): Path to the PDF file to be processed.
#     """
#     embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     file_paths=[]

#     #1.upload
#     for file in uploaded_files:
#         save_path = Path(UPLOAD_DIR) / file.filename
#         with open(save_path,"wb") as f:
#             f.write(file.file.read())
#         file_paths.append(str(save_path))
#     #2.split
#     for file_path in file_paths:
#         loader = PyPDFLoader(file_path)
#         documents = loader.load()
        
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=500,
#             chunk_overlap=100,
#             length_function=len
#         )
#         chunks= text_splitter.split_documents(documents)

#         texts = [chunk.page_content for chunk in chunks]
#         metadata =[ chunk.metadata for chunk in chunks]
#         ids =[f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

#         #3.embed and upsert
#         print(f"Embedding chunks")
#         embedding = embed_model.embed_documents(texts)

#         print(f"Upserting chunks to Pinecone")

#         with tqdm(total=len(embedding), desc="Upserting to Pinecone") as pbar:
#             index.upsert(vectors=zip(ids, embedding, metadata))
#             pbar.update(len(embedding))
def load_vectorstore(uploaded_files):
    """
    Load PDFs, split into chunks, embed them, and upsert into Pinecone.
    """
    embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths = []

    # 1. Save uploaded files
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    # 2. Process each file
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]
        metadata = [{"source": str(chunk.metadata.get("source", file_path))} for chunk in chunks]

        # 3. Embed
        print(f"Embedding {len(texts)} chunks for {file_path}...")
        embeddings = embed_model.embed_documents(texts)

        # 4. Upsert
        print(f"Upserting chunks to Pinecone...")
        vectors = [(ids[i], embeddings[i], metadata[i]) for i in range(len(embeddings))]

        with tqdm(total=len(vectors), desc="Upserting to Pinecone") as pbar:
            # You can batch this if large
            index.upsert(vectors=vectors)
            pbar.update(len(vectors))

        print(f"✅ Upserted {len(vectors)} chunks to {PINECONE_INDEX_NAME}")

    print(f"Upserted {len(embedding)} chunks to Pinecone index {PINECONE_INDEX_NAME}.")
    print(f"Upload complete for {file_path}")

    