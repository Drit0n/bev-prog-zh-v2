import scrapy
import pandas as pd
from pymongo import MongoClient

class OpenDataCsvToMongoSpider(scrapy.Spider):
    name = "zh_opendata_spider"
    start_urls = ["https://opendata.swiss/de/dataset/zukunftige-bevolkerung-kanton-zurich-und-regionen-nach-geschlecht-und-alter/resource/ad753801-25e7-4bce-b8ab-a704962c95de"]

    mongo_uri = "mongodb+srv://bevprogzh:bevprogzh@cluster0.4agtg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    mongo_db = "bev_prog_zh"
    mongo_collection = "bev_population"

    def parse(self, response):
        # CSV-Link von der Detailseite extrahieren
        csv_url = response.css('a[href$=".csv"]::attr(href)').get()
        if csv_url:
            self.log(f"✅ CSV-Link gefunden: {csv_url}")
            self.download_and_import_csv(csv_url)
        else:
            self.log("❌ Kein CSV-Link gefunden.")

    def download_and_import_csv(self, csv_url):
        # CSV direkt mit pandas von URL laden
        df = pd.read_csv(csv_url)
        df['jahr'] = df['jahr'].astype(int)

        client = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        collection = db[self.mongo_collection]

        collection.delete_many({})
        collection.insert_many(df.to_dict(orient="records"))
        self.log(f"✅ {len(df)} Datensätze direkt in MongoDB importiert.")
