from pymongo import MongoClient
import pandas as pd

MONGO_URI = "mongodb+srv://bevprogzh:bevprogzh@cluster0.4agtg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["bev_prog_zh"]
collection = db["bev_population"]

def get_data(region="all", altersgruppe="all"):
    query = {}
    if region != "all":
        query["region"] = region
    if altersgruppe != "all":
        query["alter"] = altersgruppe
    cursor = collection.find(query)
    df = pd.DataFrame(cursor)
    return df


