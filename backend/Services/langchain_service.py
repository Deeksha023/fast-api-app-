import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


env_path = Path(__file__).resolve().parent.parent / ".env"

print("ENV PATH =", env_path)
print("FILE EXISTS =", env_path.exists())

load_dotenv(env_path)

print("GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY
)



prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI career assistant. Help users with jobs, placements, resumes, interview preparation, career guidance and learning roadmaps."
    ),
    ("human", "{user_query}")
])

chain = prompt | llm



store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chat_with_memory = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_history,
    input_messages_key="user_query"
)



def ask_ai(query: str):
    response = chain.invoke(
        {
            "user_query": query
        }
    )

    return response.content


def ask_ai_with_memory(query: str, session_id: str):
    response = chat_with_memory.invoke(
        {
            "user_query": query
        },
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )

    return response.content