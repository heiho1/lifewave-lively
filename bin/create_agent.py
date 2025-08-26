#! ../lifewave-env/bin/python3
from pinecone import Pinecone
pc = Pinecone(api_key="pcsk_4UEAM7_MY5HKHJ7W6VnnBLrBpKYitHDVycJbEjWpCUqjQp1qdqnuy1dqRjLNmGY3WD1WhQ")

assistant = pc.assistant.create_assistant(
    assistant_name="lifewave-assistant", 
    instructions="Answer in polite, short sentences. Use American English spelling and vocabulary.", 
    timeout=30 # Wait 30 seconds for assistant operation to complete.
)
