from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
import os
dotenv_path='.env'
load_dotenv(dotenv_path)

model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

def document_loader(file_path):
    loader=PyPDFLoader(file_path)
    docs=loader.load()
    content=docs[0].page_content[0:]
    return content

def scanning(prompt):
    chain=prompt | model
    result=chain.invoke({"resume":docs})
    return result

def prompting(user_prompt):
    prompt=PromptTemplate.from_template("{resume} this is a resume of an applican."+'.'+user_prompt)
    return prompt

