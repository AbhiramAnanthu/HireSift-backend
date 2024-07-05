from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

dotenv_path='.env'
load_dotenv(dotenv_path)

model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
