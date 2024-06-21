from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import gradio as gr 

# Load api key to environment
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Load groq model llama3
model = ChatGroq(model_name='llama3-8b-8192')

# Chat message history
store = {}

def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_model_response(message:str, history:str)->str:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a very helpful assistant"
            ),
            MessagesPlaceholder(variable_name='history'),
            ("human", "{input}"),
        ]
    )
    runnable = prompt | model
    with_message_history = RunnableWithMessageHistory(
        runnable,
        get_session_history,
        input_messages_key = "input",
        history_messages_key = "history",
    )
    config = {'configurable':{'session_id':'abc1'}}
    response = with_message_history.invoke(
        {'input':message},
        config = config,
    )
    return response.content

demo = gr.ChatInterface(fn=get_model_response, title='Groq Llama3 Chatbot')

if __name__ == "__main__":
    demo.launch()
