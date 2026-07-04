import os

from dotenv import load_dotenv

try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory
except ImportError:
    ChatGroq = None
    ChatPromptTemplate = None
    InMemoryChatMessageHistory = None
    RunnableWithMessageHistory = None

# Load .env file
load_dotenv()

# Read API Key
API_KEY = os.getenv("GROQ_API_KEY")

# Model
LLAMA_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# -------------------------
# Lazy initialization
# -------------------------

llm = None
prompt = None
chain = None
chat_with_memory = None
store = {}


def _initialize_components():
    global llm, prompt, chain, chat_with_memory

    if llm is not None and prompt is not None and chain is not None and chat_with_memory is not None:
        return

    if ChatGroq is None or ChatPromptTemplate is None or InMemoryChatMessageHistory is None or RunnableWithMessageHistory is None:
        raise RuntimeError("LangChain Groq dependencies are not installed. Install langchain-groq and langchain-core first.")

    if not API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your environment or .env file.")

    llm = ChatGroq(model=LLAMA_MODEL, groq_api_key=API_KEY)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant."),
        ("human", "{user_query}")
    ])
    chain = prompt | llm

    def get_history(session_id: str):
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    chat_with_memory = RunnableWithMessageHistory(
        runnable=prompt | llm,
        get_session_history=get_history,
        input_messages_key="user_query"
    )


# -------------------------
# Chat without memory
# -------------------------

def chat_without_memory(query: str):
    _initialize_components()
    response = llm.invoke(query)
    return response.content


# -------------------------
# Prompt Template
# -------------------------

def chat_with_prompt(query: str):
    _initialize_components()
    response = chain.invoke({"user_query": query})
    return response.content


# -------------------------
# Chat Memory
# -------------------------

def chat(query: str, session_id: str = "user1"):
    _initialize_components()
    response = chat_with_memory.invoke(
        {"user_query": query},
        config={"configurable": {"session_id": session_id}}
    )
    return response.content


def ask_ai(query: str, session_id: str = "user1"):
    return chat(query, session_id=session_id)


# -------------------------
# Testing
# -------------------------

if __name__ == "__main__":
    try:
        print("Without Memory")
        print(chat_without_memory("What is the capital of France?"))

        print("\nPrompt")
        print(chat_with_prompt("I want to learn AI"))

        print("\nMemory")
        print(chat("I want to learn AI"))
        print(chat("Where do I learn it?"))
    except Exception as exc:
        print(f"Chat service error: {exc}")