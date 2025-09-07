from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model="qwen/qwen3-32b",
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a medical assistant. Use the provided context to answer the question.
        Your job is to provide clear, accurate and helpful responses based **only on the provided**
       
        ---
        **Context**:
        {context}

        **User Question**:
        {question}
        ---
       

        **Answer**
        -Respond in a calm , factual and respectful manner.
        -If the question is not related to the context, politely inform the user that you cannot
        answer the question based on the provided documents.
        - Do NOT make up answers or provide information that is not in the context.
        - If the context is empty, inform the user that you cannot answer the question.
        -Do not give medical advice, diagnosis, or treatment.
        """
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )