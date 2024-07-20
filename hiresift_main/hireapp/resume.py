from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_community import BigQueryVectorStore
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004", project_id="bold-site-427218-v5"
)

store = BigQueryVectorStore(
    project_id="bold-site-427218-v5",
    dataset_name="my_langchain_dataset",
    table_name="doc_and_vectors",
    location="us-central1",
    embedding=embeddings,
)


def extractor(docs):
    res_cont=[]
    file_path=docs.get('file_path')
    loader=PyPDFLoader(file_path)
    text=loader.load()
    content={
        'id':docs.get(id),
        'text':text
    }
    res_cont.append(content)
    return res_cont
