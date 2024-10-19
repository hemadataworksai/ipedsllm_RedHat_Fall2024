# Python ChatBot Application

## 1. chroma_vector_db
This directory contains a Python application that creates a collection in a Chroma vector database client and populates it with data from a JSON file.

## 2. langchain_bot
This directory contains a Python-based backend service using `FastAPI` and `Uvicorn`. It provides endpoints for:

  - Storing chat history in `Redis`
  - Utilizing user-specific chat history for real-time agent interactions
  - Retrieving `PostgreSQL` table details from a `Chroma DB` collection
  - Generating SQL queries based on user requests

The service integrates these components to efficiently fetch and process data in response to end-user queries.

## 3. streamlit_ui
This directory contains Streamlit-based frontend services that:

  - Create endpoints using `user_id` and `conversation_id`
  - Establish user sessions
  - Integrate with the Redis DB Chat History service
  - Utilize `Langserve` technology to invoke HTTP POST methods
  - Connect to the FastAPI backend modules

The frontend services manage user interactions and seamlessly communicate with the backend to provide a cohesive chat experience.