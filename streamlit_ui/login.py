from main import get_chat_session
import sys
import streamlit_authenticator as stauth
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from register import sign_up
import os
import ast
from dotenv import load_dotenv
import uuid
load_dotenv()

st.set_page_config(page_title="Login", page_icon="👋", layout="centered")


# current_dir = os.path.dirname(os.path.abspath(__file__))
# utils_dir = os.path.join(
#     current_dir, 'C:/Users/abhie/OneDrive - Northeastern University/text2sql_prod')
# sys.path.append(utils_dir)


# ==========================================================DB connection=================================================================
db_url = os.getenv("DB_URL")
print("Database connection", db_url)
db = SQLDatabase.from_uri(db_url)
query = "Select email, username, password from public.user_details"
input = db.run_no_throw(query)
credentials = {'usernames': {}}
emails = []
usernames = []
password = []
print(" Showing input ", input)
if input != '':
    for eid, un, pwd in ast.literal_eval(input):
        emails.append(eid)
        usernames.append(un)
        password.append(pwd)

    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {
            'name': emails[index], 'password': password[index]}

authenticator = stauth.Authenticate(credentials=credentials, cookie_name='Streamlit',
                                    cookie_key='abcdef', cookie_expiry_days=4, pre_authorized=False)
name, authentication_status, username = authenticator.login()

info, info1 = st.columns(2)

if username:
    if username in usernames:
        if authentication_status:
            authenticator.logout('Logout', 'main')
            conversation_id = str(uuid.uuid4())
            st.write(f'Welcome *{username}*')
            get_chat_session(username, conversation_id)
            # st.write(f'Welcome *{name}*')
        elif not authentication_status:
            with info:
                st.error('Invalid username or password')
        else:
            with info:
                st.warning('Please fill in the credentials')
    else:
        with info:
            st.warning("Username doesn't exists. Please sign up")

if not authentication_status:
    sign_up()
