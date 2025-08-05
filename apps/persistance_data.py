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
persistance_client = chromadb.PersistentClient('data_vector/persistance1')

# Membuat sebuah collection
collection = persistance_client.get_or_create_collection(
    'Peraturan_kedua',
    embedding_function= ef_googleAI,
    metadata= {
        "creator":"Muhammad Farras Ma'ruf",
        "at_place" : "Kebunsu Bogor"
    }
)

# memuat berita dari resource tipe json
df = pd.read_json(os.path.abspath("data/berita.json"))
print(df.columns) # tampilkan nama kolom


# Memberikan data pada persistance get 
# Ini hanya jalan sekali saja (karena docoument yang kita berikan selalu sama, maka saya gunnakan upsert)
collection.upsert(
    ids= [f"id_berita_ke_{a}" for a in range (len(df))],
    documents= df.isi.to_list(),
    metadatas= [{"judul":df.judul[a], "tanggal":df.tanggal[a], "lokasi":df.lokasi[a],"kategori":df.kategori[a],"sumber":df.sumber[a]} 
                for a in range(len(df))] # type: ignore
)

# Giving question
pertanyaan = ["Tradisi lomba perahu 'Pacu Jalur' dari Kabupaten Kuantan",
         "Berita tentang narkoba ?"]

# Query the collection
response = collection.query(
    query_texts=pertanyaan,
    n_results=1,
    include=["metadatas","documents","distances"]
)

pp (response)