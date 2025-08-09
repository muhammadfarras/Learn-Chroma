import chromadb
import os
from dotenv import dotenv_values as env
from chromadb.utils import embedding_functions
import pandas as pd
from pprint import pp

# Menggunakan persitance database
# Menggunakan embedding function open AI


# Load env
my_env = env(os.path.abspath(".env"))
api = my_env.get("API_OPENAI")

# Membuat embeddings function
ef_googleAI = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=api
)

# Persistance client
persistance_client = chromadb.HttpClient(host='localhost', port=9000)

# Mengambil collection yang seudah ada
collection = persistance_client.get_collection(
    'Peraturan_ketiga',
    embedding_function=ef_googleAI
)

## Mneampilkan objek collection
pp(collection.get_model().metadata)
print(f"\r\nQuery pertama",end="\r\n")

# Giving question
pertanyaan = ["Tradisi lomba perahu 'Pacu Jalur' dari Kabupaten Kuantan",
         "Berita tentang narkoba ?"]

# Query the collection
response = collection.query(
    query_texts=pertanyaan,
    n_results=1,
    include=["metadatas","documents","distances"],
)

pp (response)


print(f"\r\nQuery Kedua",end="\r\n")
# Query the collection
response = collection.query(
    query_texts=pertanyaan,
    n_results=1,
    include=["metadatas","documents","distances"],
    where={
        "lokasi":{
            "$eq" :"Kuansing, Sumatera Barat",
        }
    }
)

pp (response)