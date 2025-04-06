import pandas as pd
from pymongo import MongoClient
import os
import requests
from io import StringIO

# ✅ CSV herunterladen
csv_url = "https://www.web.statistik.zh.ch/ogd/daten/ressourcen/KTZH_00000705_00005785.csv"
response = requests.get(csv_url)
response.encoding = 'latin1'  # Wichtige Einstellung für die Zeichencodierung

# ✅ CSV-Text in Zeilen aufteilen und Header bereinigen
lines = response.text.splitlines()
if lines:
    # Entferne alle Anführungszeichen aus der Header-Zeile
    header = lines[0].replace('"', '')
    lines[0] = header
csv_data = "\n".join(lines)
csv_io = StringIO(csv_data)

# ✅ CSV korrekt einlesen – Trennzeichen ist ein Komma
df = pd.read_csv(csv_io, sep=',')

# 🔍 Spaltennamen bereinigen
df.columns = df.columns.str.strip().str.lower()

# 🧠 'jahr'-Spalte checken
if 'jahr' not in df.columns:
    print("❌ Spalte 'jahr' nicht gefunden. Gefundene Spalten:", df.columns.tolist())
    exit(1)

df['jahr'] = df['jahr'].astype(int)

# ☁️ Mit MongoDB verbinden
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("❌ MONGO_URI Umgebungsvariable ist nicht gesetzt.")
    exit(1)

client = MongoClient(mongo_uri)
db = client["bev_prog_zh"]
collection = db["bev_population"]

# Vorherige Datensätze löschen und neue einfügen
collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))

print(f"✅ {len(df)} Datensätze erfolgreich in MongoDB importiert.")
print("✅ Datenbank-Import erfolgreich!")
