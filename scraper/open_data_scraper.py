import pandas as pd
from pymongo import MongoClient
import os

# ✅ Direkter Download-Link zur CSV-Datei
csv_url = "https://www.web.statistik.zh.ch/ogd/daten/ressourcen/KTZH_00000705_00005785.csv"

# ✅ MongoDB-Zugang über Umgebungsvariable (kommt aus GitHub Secret)
mongo_uri = os.getenv("mongodb+srv://bevprogzh:bevprogzh@cluster0.4agtg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo_db = "bev_prog_zh"
mongo_collection = "bev_population"

# 📥 CSV laden
df = pd.read_csv(csv_url, sep=';', encoding='utf-8')
df["jahr"] = df["jahr"].astype(int)

# ☁️ In MongoDB speichern
client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))

print(f"✅ {len(df)} Datensätze erfolgreich in MongoDB importiert.")