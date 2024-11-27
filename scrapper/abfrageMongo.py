from pymongo import MongoClient

# Verbindung zur MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["firmendaten"]
collection = db["fullsite"]

# Textsuche mit Relevanz
results = collection.find(
    {"$text": {"$search": "services"}},
    {"score": {"$meta": "textScore"}}
).sort("score", {"$meta": "textScore"})

# Ergebnisse ausgeben
for doc in results:
    print(f"URL: {doc['url']}")
    print(f"Score: {doc['score']}")
    print(f"Cleaned Text: {doc['cleaned_text']}\n")
