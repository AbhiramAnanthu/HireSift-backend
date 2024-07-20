from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
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

prompt_template = PromptTemplate.from_template(
    "This is a prompt {prompt} given by the user to select a candidate from a set of resumes.Identify the requirements, skills, character about the candidate that the user needs from the prompt"
)

chain = prompt_template | llm


def extractor(docs):
    res_cont = []
    file_path = docs.get("file_path")
    loader = PyPDFLoader(file_path)
    text = loader.load()
    for obj in text:
        obj.id=docs.get('id')
    return text

def prompting_storing(user_input, document):
    result = chain.invoke({"prompt": user_input})
    content=[]
    for doc in document:
        resume_content=doc.page_content
        content.append(resume_content)
    store.add_texts(content)
    result=store.similarity_search(user_input,k=1)
    for obj in result:
        for doc in document:
            obj.id=doc.id
    return filtering(result)

def filtering(result):
    comparing_data=[]
    for res in result:
        id=res.id
        score=res.metadata.get('score')
        comparing_data.append({
            "id":id,
            "score":score
        })
    sorted_candidates=sorted(comparing_data,key=lambda x:x['score'],reverse=True)
    return sorted_candidates
