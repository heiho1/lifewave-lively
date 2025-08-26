#! ../lifewave-env/bin/python3
from pinecone import Pinecone
pc = Pinecone(api_key="pcsk_4UEAM7_MY5HKHJ7W6VnnBLrBpKYitHDVycJbEjWpCUqjQp1qdqnuy1dqRjLNmGY3WD1WhQ")

# Get your assistant.
assistant = pc.assistant.Assistant(
    assistant_name="lifewave-assistant", 
)

# List files in your assistant.
files = assistant.list_files()
