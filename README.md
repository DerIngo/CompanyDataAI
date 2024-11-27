# CompanyDataAI
PoC to gather data from company websites and an web interface to ask an AI about it

1. Clone Repository
2. Create virtual environment and install requirements:
```bash
# Python virtual Environment
python -m venv CompanyDataAI
## Activate
source CompanyDataAI/bin/activate

# Install requirements
pip install -r requirements.txt
```
3. Start MongoDB
```bash
docker stop CompanyDataAI-mongo && docker rm CompanyDataAI-mongo
docker run --name CompanyDataAI-mongo -d -p 27017:27017 mongo
```
4. Create Index
Open Mongo Client and execute:
```bash
db.fullsite.dropIndexes();
db.fullsite.createIndex(
  { cleaned_text: "text" },  // Das Feld, das durchsucht werden soll
  { default_language: "german" }  // Sprache für den Textindex
);
```
