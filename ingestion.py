import os
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv(override=True)

# 1. Initialize clients
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

pinecone_client = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index_name = os.getenv("PINECONE_INDEX_NAME")

index = pinecone_client.Index(index_name)

# 2. Read TXT files
data_path = Path("Generative_AI_Training/Data/info")

documents = []

for file in data_path.glob("*.txt"):
    content = file.read_text(encoding="utf-8")

    documents.append({
        "content": content,
        "source": file.name
    })
#print(documents)
print(f"Loaded {len(documents)} documents")

# 3. Split text into chunks
def split_text(text, chunk_size=5000):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size

    return chunks

# 4. Generate embeddings and prepare vectors
vectors = []

for document in documents:

    chunks = split_text(document["content"])

    for chunk in chunks:

        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )

        embedding = response.data[0].embedding

        vector_id = hashlib.sha256(
            f'{document["source"]}:{chunk}'.encode("utf-8")
        ).hexdigest()

        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {
                "source": document["source"],
                "text": chunk
            }
        })


#print(vectors[0]['id'])
print(f"Created {len(vectors)} vectors") 

# 5. Upload vectors to Pinecone
if vectors:
    index.upsert(
        vectors=vectors,
        namespace="rag-demo"
    )

print("Successfully ingested documents into Pinecone!")
print(f"Total documents: {len(documents)}")
print(f"Total vectors: {len(vectors)}")
