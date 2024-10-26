import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()

CHROMADB_HOST = os.getenv('CHROMADB_HOST')
CHROMADB_PORT = os.getenv('CHROMADB_PORT')
settings = Settings(anonymized_telemetry=False, allow_reset=True,chroma_server_host=CHROMADB_HOST,chroma_server_http_port=CHROMADB_PORT,chroma_server_api_default_path= "/api/v1" )


try:
    client = chromadb.Client(settings=settings)
    collection_name = os.getenv('COLLECTION_NAME')
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
        return metadata
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    embedding_function = OpenAIEmbeddings(
        openai_api_key=openai_api_key, model=os.getenv('TEXT_EMBEDDING'))

    file_path = os.getenv('JSON_FILE_PATH')
    loader = JSONLoader(
        file_path=file_path,
        jq_schema=".[].Table_Info[]",
        content_key="Table_Description",
        metadata_func=metadata_func,
    )
    data = loader.load()
    
    vectorstore = Chroma(client=client, collection_name=collection_name,
                     embedding_function=embedding_function)
    uuids = [str(uuid4()) for _ in range(len(data))]
    
    vectorstore.add_documents(documents=data, ids=uuids)

    print("Data loaded successfully into ChromaDB collection:", collection_name)

except Exception as e:
    print("Error:", e)
