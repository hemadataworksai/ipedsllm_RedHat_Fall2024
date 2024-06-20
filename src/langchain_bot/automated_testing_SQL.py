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
# import Levenshtein as le


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
# LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
db_url = os.getenv("DB_URL_1")

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
    chain = (
        RunnablePassthrough.assign(context=context_chain, table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query)
    )
    return chain

def query_chatbot_for_sql(question):
    standalone_messages = [{"role": "user", "content": question}]
    chain = get_testing_chain()
    response = chain.invoke({"question": question, "top_k": 3, "messages": standalone_messages})
    return response['query']

def get_output_chain(sql):
    db = SQLDatabase.from_uri(db_url)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    context_chain = (
        {"context": itemgetter("question") | retriever,
         "question": itemgetter("question")}
        | retriever_prompt
        | model
        | StrOutputParser()
    )
    generate_query = lambda context: sql
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(context=context_chain, table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )
    return chain

def output_chatbot_for_sql(sql):
    standalone_messages = [{"role": "user", "content": question}]
    chain = get_output_chain(sql)
    response = chain.invoke({"question": question, "top_k": 3, "messages": standalone_messages})
    return response

def replace_space(input, replacement=''):
    result = input.replace('\n', replacement)
    result = result.replace(' ', replacement)
    return result

# Load test cases
df = pd.read_excel('./Questions.xlsx', sheet_name="Sheet3")
print(df.columns)

test_results = []
for index, row in df.iterrows():
    question = str(row['Human Language ']).strip() if pd.notna(row['Human Language ']) else ""
    expectation = str(row['Expected SQL Query']).strip() if pd.notna(row['Expected SQL Query']) else ""
    expected_sql = replace_space(expectation)
    
    if question:
        generation = query_chatbot_for_sql(question)
        generated_sql = replace_space(generation)
        is_correct = (generated_sql == expected_sql)
        expected_output = output_chatbot_for_sql(expectation)
        generated_output = output_chatbot_for_sql(generation)
        if not is_correct:
            is_same = (expected_output == generated_output)
            status = "Output Correct" if is_same else "Output Incorrect"
        else:
            status = "SQL Query Correct"
        # status = "Correct" if is_correct else "Incorrect"
        # distance = le.distance(expected_sql, generated_sql)
        # max_length = max(len(expected_sql), len(generated_sql))
        # similarity = (1 - distance / max_length) * 100
        test_results.append({
            "Question": question,
            "Expected SQL": expectation,
            "Generated SQL": generation,
            "Expected Output": expected_output,
            "Generated Output": generated_output,
            "Status": status
            # "Similarity": similarity
        }) 
        
        # Introduce delay to avoid hitting rate limits
        time.sleep(10)

print("Testing is completed. Next is the output result.\n")
results = pd.DataFrame(test_results)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(results)
# Save results to Excel
results_df = pd.DataFrame(test_results)
results_df.to_excel('test_results_sql.xlsx', index=False)
print("Testing completed. Results are saved in 'test_results_sql.xlsx'.")

total_count = len(results)
correct_count = results[results['Status'].isin(['Output Correct', 'SQL Query Correct'])].shape[0]
accuracy = correct_count / total_count * 100
print(f"The accuracy of this test is {accuracy:.2f}%")
