import streamlit_authenticator as stauth
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from register import sign_up
import os
import ast
from dotenv import load_dotenv
from main import main
load_dotenv()

st.set_page_config( page_title="Login", page_icon="👋", layout="centered")
# st.markdown("# Login")

#==========DB connection==============
db_url = os.getenv("DB_URL")
db = SQLDatabase.from_uri(db_url)
query = "Select email, username, password from public.user_details"
input = db.run_no_throw(query)
credentials = {'usernames': {}}
emails = []
usernames = []
password = []

if input != '':
    for eid, un, pwd in ast.literal_eval(input):
        emails.append(eid)
        usernames.append(un)
        password.append(pwd)
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': password[index]}


authenticator = stauth.Authenticate(credentials=credentials, cookie_name='Streamlit', cookie_key='abcdef', cookie_expiry_days=4, pre_authorized = False)
name, authentication_status, username = authenticator.login()
info, info1 = st.columns(2)
if username:
    if username in username:
        if authentication_status:
            authenticator.logout('Logout', 'main')
            main(username)
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
