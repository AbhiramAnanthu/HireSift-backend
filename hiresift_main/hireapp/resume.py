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
    prompt = {
        "resume": document_loader(file_path),
        "user_prompt": "check whether this applicant show any skills to be a software developer",
    }
    result = agent.invoke(prompt).content
    return {
        "result": result,
        "prompt": f"{prompt.get('resume')} is a resume of an applicant.{prompt.get('user_prompt')}",
    }


def filtering(result):
    content = result.get("result")
    file_path = result.get("file_path")
    prompt_text = """You are an AI agent responsible for ranking a list of job candidates based on the similarity of their resumes to an employee profile provided. 
    The task is to analyze the resumes and rank the candidates from highest to lowest similarity, including the percentage of similarity for each candidate. 
    Here's the employee profile and the list of candidate resumes: {content}. Here is the employee prompt {prompt}
    output formate : 
    1. Candidate A: XX/%/ similarity
    2. Candidate B: XX/%/ similarity
    3. Candidate C: XX/%/ similarity
    """
    prompt_template = PromptTemplate.from_template(prompt_text)
    loader = scanning(file_path)
    prompt = loader["prompt"]
    chain = prompt_template | llm
    ranking = chain.invoke({"content": content, "prompt": prompt})
    return {"ranking": ranking, "file_path": file_path, "id": result.get("id")}

