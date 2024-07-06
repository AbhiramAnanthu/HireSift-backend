from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash')

def document_loader(file_path):
    loader=PyPDFLoader(file_path)
    resume=loader.load()
    content=resume[0].page_content[0:]
    return content

def scanning(file_path):
    prompt=PromptTemplate.from_template("{resume} is a resume of an applicant.{user_prompt}")
    agent=prompt | llm
    result=agent.invoke({"resume":document_loader(file_path),"user_prompt":"check whether this applicant show any skills in machine learning and ai"}).content
    return result





