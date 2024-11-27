from flask import Flask, render_template, request
from pymongo import MongoClient
from openai import OpenAI

# Flask-App initialisieren
app = Flask(__name__)

# Verbindung zur MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["firmendaten"]
collection = db["fullsite"]

# Verbindung zur lokalen KI
local_ai = OpenAI(base_url="http://172.23.32.1:1234/v1", api_key="lm-studio")
#model = "xtuner/llava-phi-3-mini-gguf",  # Modellname
model = "mradermacher/Teuken-7B-instruct-commercial-v0.4-GGUF"

def search_mongodb(question):
    """
    Führt eine Volltextsuche in MongoDB aus und gibt die relevantesten Ergebnisse zurück.
    """
    results = collection.find(
        {"$text": {"$search": question}},  # Volltextsuche
        {"score": {"$meta": "textScore"}}  # Suchrelevanz
    ).sort("score", {"$meta": "textScore"}).limit(3)  # Begrenze auf 3 Ergebnisse

    # Kürze die Texte
    trimmed_results = []
    for doc in results:
        text = doc['cleaned_text'][:1000]  # Kürze den Text auf 1000 Zeichen
        trimmed_results.append({**doc, "cleaned_text": text})

    return trimmed_results

def generate_response(question, results):
    """
    Generiert eine Antwort mit der lokalen KI basierend auf den MongoDB-Ergebnissen.
    """
    # Kontext aus den MongoDB-Ergebnissen erstellen
    context = "\n".join(
        [f"URL: {doc['url']}\nText: {doc['cleaned_text']}" for doc in results]
    )

    # Nachrichtenformat für die KI
    messages = [
        {"role": "system", "content": "Du bist ein virtueller Assistent, der Fragen zu Firmendaten beantwortet."},
        {"role": "user", "content": f"Hier sind die Daten:\n{context}\n\nFrage: {question}"}
    ]

    # Anfrage an die lokale KI
    response = local_ai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Startseite mit Eingabeformular.
    """
    if request.method == 'POST':
        question = request.form['question']
        
        # Suche in MongoDB
        results = search_mongodb(question)

        # Keine Ergebnisse gefunden
        if not results:
            return render_template('result.html', question=question, response="Keine relevanten Daten gefunden.")

        # KI-Antwort generieren
        response = generate_response(question, results)
        return render_template('result.html', question=question, response=response)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
