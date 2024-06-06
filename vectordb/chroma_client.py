import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ChromaDB server configuration
CHROMADB_HOST = "chroma"
CHROMADB_PORT = 8000  # Adjust if your ChromaDB server is running on a different port

# ChromaDB client settings
settings = Settings(allow_reset=True)

try:
    # Initialize ChromaDB client
    client = chromadb.HttpClient(
        host=CHROMADB_HOST, port=CHROMADB_PORT, settings=settings)

    # Create or connect to the collection
    collection_name = "ipeds_llm"  # Adjust as needed
    collection = client.get_or_create_collection(collection_name)

    def metadata_func(record: dict, metadata: dict) -> dict:
        def column_retriever(ls):
            cname = []
            dtype = []
            cdesc = []
            for i in range(len(ls)):
                cname.append(record.get("Columns")[i].get("Column_Name"))
                dtype.append(record.get("Columns")[i].get("Data_Type"))
                cdesc.append(record.get("Columns")[
                             i].get("Column_Description"))
            return cname, dtype, cdesc
        cname, dtype, cdesc = column_retriever(record.get("Columns"))

        metadata["Table_Name"] = record.get("Table_Name")
        metadata["Table_Description"] = record.get("Table_Description")
        metadata["Column_Names"] = str(cname)
        metadata["Data_Type"] = str(dtype)
        metadata["Column_Description"] = str(cdesc)
        # metadata["share"] = record.get("share")
        return metadata

    # Embedding function
    openai_api_key = os.getenv("OPENAI_API_KEY")  # Adjust if necessary
    embedding_function = OpenAIEmbeddings(
        openai_api_key=openai_api_key, model="text-embedding-ada-002")

    # Load data from JSON file
    file_path = "tableinfo.json"  # Adjust the file path as needed
    loader = JSONLoader(
        file_path=file_path,
        jq_schema=".[].Table_Info[]",
        content_key="Table_Name",
        metadata_func=metadata_func,
    )
    data = loader.load()

    # Add documents to the collection
    for doc in data:
        content = doc["content"]
        embeddings = embedding_function.embed(content)
        metadata = doc["metadata"]
        collection.add(content, embeddings, metadata)

    print("Data loaded successfully into ChromaDB collection:", collection_name)

except Exception as e:
    print("Error:", e)

# To create a local chroma server-
# docker pull chromadb/chroma
# docker run -p 8000:8000 chromadb/chroma
