# Deployment

## 1. postgres
postgres-services.yaml file manifest creates a Kubernetes Deployment to run a single instance of a PostgreSQL container. The PostgreSQL service is configured with the necessary credentials and connection information to access a managed database hosted on DigitalOcean.


  - `POSTGRES_DB_NAME`: The name of the PostgreSQL database created in PostgreSQL.
  - `POSTGRES_DB_USERNAME`: An environment variable for the database username.
  - `POSTGRES_DB_PASSWORD`: An environment variable for the database password.
  - `POSTGRES_DB_HOST`: This environment variable contain the hostname or IP address of your PostgreSQL service on DigitalOcean.
  - `POSTGRES_DB_PORT`: The port number on which PostgreSQL is running on Digital Ocean.
  - `POSTGRES_DB_URL`: This environment variable contain the database URL containing hostname, username, password, host and port of your PostgreSQL service on DigitalOcean.



## 2. redis_db
postgres-services.yaml file configures a Redis instance within Kubernetes that connects to an Upstash-hosted Redis database, which will store and manage chatbot conversation history.

  -  Upstash provides a serverless Redis solution, which means the Redis instance is hosted and managed by Upstash. You can connect to it via an endpoint `UPSTASH_URL` and authenticate using the `UPSTASH_TOKEN`.
  - The Redis instance hosted on Upstash will be used to store chat history for the chatbot. For each user, Redis will store the chat history based on a specific conversation ID, which can be the key for accessing that user's chat history.
  - This allows for fast retrieval of past conversations, helping the chatbot maintain context across sessions.

