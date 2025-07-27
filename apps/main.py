import chromadb
import os
import uuid

client = chromadb.Client()

# Membua sebuah collection
collection = client.create_collection("peraturan_rumah")

path_peraturan = os.path.abspath("data/peraturan_rumah.txt")

with open (path_peraturan, mode="r", encoding="utf-8") as f:
    kebijakan = f.read().splitlines()
    
collection.add(
    ids=[str(uuid.uuid4()) for a in kebijakan],
    documents=kebijakan,
    metadatas=[{"kebijakan":a} for a in range(len(kebijakan))]
)

pertanyaan=[
        "Siapa yang tidak sekolah ?"
    ]

query_response = collection.query(
    query_texts=pertanyaan,
    n_results=2
)

for number,a in enumerate(query_response["documents"]):
    print(f"Pertanyaan ({number}) : {pertanyaan[number]}")
    print(f"Jawaban : ","****\r\n****".join(a))

