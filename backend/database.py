from pymongo import MongoClient
import pandas as pd

# MongoDB Verbindungszeichenfolge (stellen Sie sicher, dass diese korrekt ist)
MONGO_URI = "mongodb+srv://bevprogzh:bevprogzh@cluster0.4agtg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB-Client initialisieren
client = MongoClient(MONGO_URI)
db = client["bev_prog_zh"]
collection = db["bev_population"]

def get_data(region="all", altersgruppe="all"):
    """
    Holt die Bevölkerungsdaten aus der MongoDB-Datenbank basierend auf den übergebenen Parametern.

    :param region: Die Region, die gefiltert werden soll, oder "all" für alle Regionen
    :param altersgruppe: Die Altersgruppe, die gefiltert werden soll, oder "all" für alle Altersgruppen
    :return: Ein DataFrame mit den gefilterten Bevölkerungsdaten
    """
    query = {}
    
    # Filter für Region und Altersgruppe anwenden
    if region != "all":
        query["region"] = region
    if altersgruppe != "all":
        query["alter"] = altersgruppe
    
    # Zähle die Anzahl der Dokumente
    count = collection.count_documents(query)  # count_documents auf der Collection anwenden

    # Wenn keine Daten vorhanden sind, ein leeres DataFrame zurückgeben
    if count == 0:
        print(f"⚠️ Keine Daten für die Region '{region}' und Altersgruppe '{altersgruppe}' gefunden.")
        return pd.DataFrame()  # Leeres DataFrame zurückgeben
    
    # Daten aus MongoDB sammeln
    cursor = collection.find(query)
    
    # Cursor in ein DataFrame umwandeln und zurückgeben
    df = pd.DataFrame(list(cursor))
    
    # Überflüssige MongoDB _id Spalte entfernen
    if "_id" in df.columns:
        df = df.drop("_id", axis=1)
    
    return df