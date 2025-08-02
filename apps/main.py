import chromadb
import os
from pprint import pp

path_peraturan = os.path.abspath("data/peraturan_rumah.txt")

with open (path_peraturan, mode="r", encoding="utf-8") as f:
    kebijakan = f.read().splitlines()

# Object Client
client = chromadb.Client()

# Membuat sebuah collection
collection = client.create_collection("peraturan_rumah")

# To generate ID per chuking data
idGenerate = [f"id{a}" for a in range (1, len(kebijakan)+1)]

collection.add(
    ids=idGenerate,
    documents=kebijakan,
    metadatas=[{"kebijakan":a} for a in range(len(kebijakan))]
)

pertanyaan=[
        "Siapa yang tidak sekolah ?",
        "Apa tugas hilyah"
    ]

query_response = collection.query(
    query_texts=pertanyaan,
    n_results=2
)

for number,a in enumerate(query_response["documents"]): # type: ignore
    pp(f"Pertanyaan ({number}) : {pertanyaan[number]}")
    pp(a)
