import pandas as pd
from pymongo import MongoClient
import os

# ✅ Direkter Download-Link zur CSV-Datei vom Statistikportal Zürich
csv_url = "https://www.web.statistik.zh.ch/ogd/daten/ressourcen/KTZH_00000705_00005785.csv"

# ✅ MongoDB-Zugang via GitHub Action Secret (NICHT direkt eintragen!)
mongo_uri = os.getenv("MONGO_URI")  # <- Wichtig: kommt aus GitHub Secret
mongo_db = "bev_prog_zh"
mongo_collection = "bev_population"

# 📥 CSV laden mit korrekter Trennung und Encoding
df = pd.read_csv(csv_url, sep=';', encoding='latin1', quotechar='"')

# 🧠 Optional: 'jahr' als Integer casten (nur wenn vorhanden)
if 'jahr' in df.columns:
    df["jahr"] = df["jahr"].astype(int)
else:
    print("❌ Spalte 'jahr' nicht gefunden. Verfügbare Spalten:")
    print(df.columns.tolist())
    exit(1)

# ☁️ In MongoDB speichern
client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))

print(f"✅ {len(df)} Datensätze erfolgreich in MongoDB importiert.")

