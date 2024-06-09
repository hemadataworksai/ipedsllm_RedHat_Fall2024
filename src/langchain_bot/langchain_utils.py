import streamlit as st
# from main import st
from src.langchain_bot.prompts import final_prompt, answer_prompt
from src.langchain_bot.table_details import table_chain as select_table
from src.langchain_bot.vector_store import retriever, retriever_prompt, model
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
# from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import (
    UpstashRedisChatMessageHistory,
)
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities.sql_database import SQLDatabase
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
db_url = os.getenv("DB_URL")
redis_url = os.getenv("UPSTASH_URL")
redis_token = os.getenv("UPSTASH_TOKEN")




@st.cache_resource
def get_chain():
    print("Creating chain")
    db = SQLDatabase.from_uri(db_url)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    context_chain = (
        {"context": itemgetter("question") | retriever,
         "question": itemgetter("question")}
        | retriever_prompt
        | model
        | StrOutputParser()
    )
    generate_query = create_sql_query_chain(llm, db, final_prompt)
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    # chain = generate_query | execute_query
    chain = (
        RunnablePassthrough.assign(context=context_chain, table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )

    return chain


def create_history(messages, session_id):
    # # Generate a unique session ID for the user
    # if 'session_id' not in st.session_state:
    #     st.session_state.session_id = str(uuid.uuid4())

    # # Fetch the session ID from session state
    # session_id = st.session_state.session_id

    # # Display the session ID for debugging purposes
    # st.write(f"Session ID: {session_id}")

    history = UpstashRedisChatMessageHistory(
        url=redis_url, token=redis_token, ttl=0, session_id=session_id)
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history


def invoke_chain(question, messages, session_id):
    chain = get_chain()
    history = create_history(messages,session_id)
    response = chain.invoke(
        {"question": question, "top_k": 3, "messages": history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response
