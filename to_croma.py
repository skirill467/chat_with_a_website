from pymongo import MongoClient
import chromadb
import requests
import json
import os

from dotenv import load_dotenv

#load api key
load_dotenv()

# MongoDB connection details
mongo_uri = 'mongodb://localhost:27017/'
mongo_db = 'web_scraper'
mongo_collection = 'scraped_data'

# ChromaDB connection details (modify according to your actual ChromaDB setup)
chroma_client = chromadb.Client()
chroma_collection = chroma_client.create_collection(name="my_collection")

# Connect to MongoDB
mongo_client = MongoClient(mongo_uri)
db = mongo_client[mongo_db]
collection = db[mongo_collection]

# Retrieve data from MongoDB
documents = collection.find()

# Function to insert data into ChromaDB
def insert_into_chromadb(url, text, id):
    # Example code to insert into ChromaDB; modify as per your ChromaDB client's API
    document = {
        "url": url,
        "text": text
    }
    chroma_collection.add(
        documents=[text + f'\n web link to get more information: {url}'],
        metadatas=[{'url' : url}],
        ids=[id]
    )

# Insert data into ChromaDB
for document in documents:
    url = document['url']
    text = document['text']
    id = document['_id']
    insert_into_chromadb(url, text, str(id))


#input question, i.e. What Swimming Pools are in North York
q = input("Ask a question about the city of Toronto:\n")

results = chroma_collection.query(
    query_texts=[q], # Chroma will embed this for you
    n_results=2 # how many results to return
)


print(results['documents'][0])
print('')
print ('------ GPT ------------')
user_text =  ' '.join(results['documents'][0]) 

openai_api_key = os.getenv("API_KEY")


url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "you are a City of Toronto support assistant. Provide also a web link at the end of the response."
        },
        {
            "role": "user",
            "content": f"Answer the client's question {q} using the following text: \n\n {user_text}"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    print("Response from OpenAI:", response.json())
    print('\n')
    print(response.json()['choices'][0]['message']['content'])
else:
    print("Error:", response.status_code, response.text)

# Close MongoDB connection
mongo_client.close()
