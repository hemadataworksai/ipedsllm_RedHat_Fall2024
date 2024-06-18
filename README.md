# text2sql_prod

# Deployment Plan

1. Setup Chroma client for hosting the KnowledgeBase
2. Establish Connection for ChromaDB
3. Setup Redis DB for message history
4. Establish Connection for Redis
5. Create API & endpoints for services - langchain_bot(Application Logic), streamlit-app(Frontend UI)
6. Create Docker images for services - langchain_bot, streamlit-app, Postgres, Chroma and Redis
7. Define multi-container application with docker-compose.yaml file
8. Build and Run with "docker-compose up --build"

# Kuberanates command
1. $ kubectl version
2. $ kubectl create -f etcd-operator-crd.yaml
3. $ kubectl get crd
4. $ kubectl create -f etcd-operator-sa.yaml
5. $ kubectl get serviceaccounts
5. $ kubectl create -f etcd-operator-role.yaml
6. $ kubectl create -f etcd-operator-rolebinding.yaml
7. $ kubectl create -f etcd-operator-deployment.yaml
8. $ kubectl get deployments
9. $ kubectl get pods
