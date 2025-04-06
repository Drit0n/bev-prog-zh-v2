import pandas as pd
from pymongo import MongoClient
import os
import requests
from io import StringIO

# ✅ CSV richtig manuell herunterladen
csv_url = "https://www.web.statistik.zh.ch/ogd/daten/ressourcen/KTZH_00000705_00005785.csv"
response = requests.get(csv_url)
response.encoding = 'latin1'  # wichtig!
csv_data = StringIO(response.text)

# ✅ Manuell korrekt einlesen
df = pd.read_csv(csv_data, sep=';', quotechar='"')

# 🔍 Spalten bereinigen
df.columns = df.columns.str.replace('"', '').str.strip().str.lower()

# 🧠 'jahr'-Spalte checken
if 'jahr' not in df.columns:
    print("❌ Spalte 'jahr' nicht gefunden. Spalten:", df.columns.tolist())
    exit(1)

df['jahr'] = df['jahr'].astype(int)

# ☁️ MongoDB
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["bev_prog_zh"]
collection = db["bev_population"]

collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))

print(f"✅ {len(df)} Datensätze erfolgreich in MongoDB importiert.")
