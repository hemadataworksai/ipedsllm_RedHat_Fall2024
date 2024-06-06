import streamlit as st
from src.langchain_bot.prompts import final_prompt, answer_prompt
from src.langchain_bot.table_details import table_chain as select_table
import chromadb
from chromadb.config import Settings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.memory import ChatMessageHistory
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities.sql_database import SQLDatabase

from langchain_community.chat_message_histories import (
    UpstashRedisChatMessageHistory,
)

from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import os
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
db_url = os.getenv("DB_URL_1")
redis_url = os.getenv("UPSTASH_URL")
redis_token = os.getenv("UPSTASH_TOKEN")

# ChromaDB server configuration
CHROMADB_HOST = "localhost"
CHROMADB_PORT = 8000  # Adjust if your ChromaDB server is running on a different port
# ChromaDB client settings
settings = Settings(allow_reset=True)

client = chromadb.HttpClient(
    host=CHROMADB_HOST, port=CHROMADB_PORT, settings=settings)
# Initialize the vector store
embedding_function = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002"
)

vectorstore = Chroma(client=client, collection_name="ipeds_llm",
                     embedding_function=embedding_function)

retriever = vectorstore.as_retriever()

# Define your template
template = """Answer the question based only on the following context:
{context}
Search for the table descriptions in the context and accordingly search for column names and associated column description. Include only relevant tables and columns which can be used by the downstream Text-to-SQL Agent to create SQL Queries for generating answer.
Search for any information performing the following tasks:
1. Table Names
2. Table Descriptions
3. Column Names
4. Column Descriptions
5. Encoded Values
Finally, only return table names, column names and Encoded Values only (if available).

Question: {question}
"""
retriever_prompt = ChatPromptTemplate.from_template(template)


@st.cache_resource
def get_chain():
    print("Creating chain")
    db = SQLDatabase.from_uri(db_url)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    context_chain = (
        {"context": itemgetter("question") | retriever,
         "question": itemgetter("question")}
        | retriever_prompt
        | llm
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


def create_history(messages):
    history = UpstashRedisChatMessageHistory(
        url=redis_url, token=redis_token, ttl=0, session_id="my-test-session")
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history


def invoke_chain(question, messages):
    chain = get_chain()
    history = create_history(messages)
    response = chain.invoke(
        {"question": question, "top_k": 3, "messages": history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response
