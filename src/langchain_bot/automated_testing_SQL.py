import pandas as pd
import time
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
import os
from dotenv import load_dotenv
from vector_store import retriever, retriever_prompt, model
from langchain_core.output_parsers import StrOutputParser
from table_details import table_chain as select_table
from langchain_core.runnables import RunnablePassthrough
from prompts import final_prompt, answer_prompt


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
db_url = os.getenv("DB_URL")

def get_testing_chain():
    print("Creating testing chain")
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
    # No need to execute the query in testing, just generate it
    chain = (
        RunnablePassthrough.assign(context=context_chain, table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=lambda ctx: ctx['query']
        )
    )
    return chain

def query_chatbot_for_sql(question):
    standalone_messages = [{"role": "user", "content": question}]
    chain = get_testing_chain()
    response = chain.invoke({"question": question, "top_k": 3, "messages": standalone_messages})
    return response['result']

# Load test cases
df = pd.read_excel('/Users/sankalpbiswal/ipedsllm/Tesing_DataworksAI_excel/Testing_DataworksAI_Text_to_SQL_Spring2024(1).xlsx')
print(df.columns)

test_results = []
for index, row in df.iterrows():
    question = str(row['Human Language ']).strip() if pd.notna(row['Human Language ']) else ""
    expected_sql = str(row['Expected SQL Query']).strip() if pd.notna(row['Expected SQL Query']) else ""
    
    if question:
        generated_sql = query_chatbot_for_sql(question)
        is_correct = (generated_sql == expected_sql)
        status = "Correct" if is_correct else "Incorrect"
        test_results.append({
            "Question": question,
            "Expected SQL": expected_sql,
            "Generated SQL": generated_sql,
            "Status": status
        })
        
        # Introduce delay to avoid hitting rate limits
        time.sleep(10)

# Save results to Excel
results_df = pd.DataFrame(test_results)
results_df.to_excel('test_results_sql.xlsx', index=False)
print("Testing completed. Results are saved in 'test_results_sql.xlsx'.")
