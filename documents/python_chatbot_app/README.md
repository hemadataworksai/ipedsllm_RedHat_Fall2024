# Python ChatBot Application

## 1. chroma_vector_db
<p>This directory contains a Python application that creates a collection in a Chroma vector database client and populates it with data from a JSON file.</p>

## 2. langchain_bot
<p>This directory contains a Python-based backend service using FastAPI and Uvicorn. It provides endpoints for:
<ul>
<li>Storing chat history in Redis</li>
<li>Utilizing user-specific chat history for real-time agent interactions</li>
<li>Retrieving PostgreSQL table details from a Chroma DB collection</li>
<li>Generating SQL queries based on user requests</li>
</ul>
The service integrates these components to efficiently fetch and process data in response to end-user queries.</p>

## 3. streamlit_ui
<p>This directory contains Streamlit-based frontend services that:

<li>Create endpoints using user_id and conversation_id</li>
<li>Establish user sessions</li>
<li>Integrate with the Redis DB Chat History service</li>
<li>Utilize Langserve technology to invoke HTTP POST methods</li>
<li>Connect to the FastAPI backend modules</li>

The frontend services manage user interactions and seamlessly communicate with the backend to provide a cohesive chat experience.</p>