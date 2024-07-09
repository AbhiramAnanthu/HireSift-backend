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
    model="models/text-embedding-004",project_id="bold-site-427218-v5"
)

store = BigQueryVectorStore(
    project_id="bold-site-427218-v5",
    dataset_name='my_langchain_dataset',
    table_name='doc_and_vectors',
    location='us-central1',
    embedding=embeddings,
)

def document_loader(file_path):
    loader = PyPDFLoader(file_path)
    resume = loader.load()
    content = resume[0].page_content[0:]
    return content


def scanning(file_path):
    prompt_template = PromptTemplate.from_template(
        "{resume} is a resume of an applicant.{user_prompt}"
    )
    agent = prompt_template | llm
    prompt={
            "resume": document_loader(file_path),
            "user_prompt": "check whether this applicant show any skills to be a software developer",
        }
    result = agent.invoke(prompt).content
    return {
        "result":result,
        "prompt":f"{prompt.get('resume')} is a resume of an applicant.{prompt.get('user_prompt')}"
    }

def vector(content):
    return Document(
        page_content=content,
    )

def vector_search(document,file_path):
    store.add_documents(
        document
    )
    load_query=scanning(file_path)
    user_quer_text=load_query['prompt']
    # query_vector=embeddings.embed_query(user_quer_text)
    #print(user_quer_text)
    docs= store.similarity_search(user_quer_text)
    return docs[0].page_content
