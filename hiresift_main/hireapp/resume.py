from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004", project_id="bold-site-427218-v5"
)
store = Chroma(
    collection_name="resume",
    embedding_function=embeddings,
)

prompt_template = PromptTemplate.from_template(
    "This is a prompt {prompt} given by the user to select a candidate from a set of resumes.Identify the requirements, skills, character about the candidate that the user needs from the prompt"
)

chain = prompt_template | llm


def extractor(docs):
    file_path = docs.get("file_path")
    loader = PyPDFLoader(file_path)
    text = loader.load()
    for obj in text:
        obj.id = docs.get("id")
    return text


def prompting_storing(user_input, document):
    text=[]
    score=[]
    for doc in document:
        id=doc.get('id')
        page_content=doc.get('page_content')
        text.append(page_content)
    store.add_texts(texts=text)
    result = store.similarity_search_with_score(user_input)
    for i, doc in zip(result, document):
        for score_value in i:
            if isinstance(score_value, float):
                score.append({
                    "id": doc.get('id'),
                    "score": score_value
                })
        
    sorted_candidates = sorted(score, key=lambda x: x["score"], reverse=True)
    return sorted_candidates
