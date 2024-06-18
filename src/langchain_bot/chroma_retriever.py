from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
