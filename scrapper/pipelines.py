# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import json

class MongoPipeline:

    def __init__(self):
        import os
        print(os.getcwd())
        # Lade Konfiguration aus der JSON-Datei
        with open('config.json') as config_file:
            config = json.load(config_file)
            self.mongo_uri = config['MONGO_URI']
            self.mongo_db = config['MONGO_DATABASE']

    def open_spider(self, spider):
        # Verbindung zu MongoDB herstellen
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # Verbindung schließen
        self.client.close()

    def process_item(self, item, spider):
        # Daten in die MongoDB speichern
        collection = self.db[spider.name]
        collection.insert_one({
            'url': item['url'],
            'raw_html': item['raw_html'],
            'cleaned_text': item['cleaned_text'],
            'timestamp': item['timestamp'],
        })
        return item
