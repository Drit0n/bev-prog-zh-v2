import os
from azure.storage.blob import BlobServiceClient
import argparse

try:
    print("🚀 Azure Blob Storage Upload gestartet")

    # 🔧 Argument parser: erwartet Connection-String per Argument
    parser = argparse.ArgumentParser(description='Upload Model')
    parser.add_argument('-c', '--connection', required=True, help="Azure storage connection string")
    args = parser.parse_args()

    # 📦 Azure Blob Service einrichten
    blob_service_client = BlobServiceClient.from_connection_string(args.connection)

    # 📂 Container & Modellname
    container_name = "bevprogzh-models"
    model_filename = "region_age_combined_model.pkl"

    # ✅ Relativer Pfad zum Modell (plattformunabhängig)
    script_dir = os.path.dirname(__file__)
    local_model_path = os.path.join(script_dir, model_filename)

    if not os.path.exists(local_model_path):
        raise FileNotFoundError(f"❌ Modell-Datei nicht gefunden: {local_model_path}")

    print(f"📁 Modell gefunden unter: {local_model_path}")

    # 🔎 Container prüfen oder erstellen
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.get_container_properties()
        print(f"ℹ️ Container '{container_name}' existiert bereits.")
    except Exception:
        print(f"📦 Container '{container_name}' existiert nicht. Wird erstellt...")
        blob_service_client.create_container(container_name)

    # 🔢 Vorhandene Versionen abrufen
    blobs = container_client.list_blobs()
    existing_versions = [
        int(blob.name.split("_")[-1].replace(".pkl", ""))
        for blob in blobs
        if blob.name.startswith("region_age_combined_model_") and blob.name.endswith(".pkl")
    ]
    new_version = max(existing_versions, default=0) + 1
    new_blob_name = f"region_age_combined_model_{new_version}.pkl"

    print(f"📤 Upload als: {new_blob_name}")

    # 🔼 Hochladen
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=new_blob_name)
    with open(local_model_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"✅ Modell erfolgreich als '{new_blob_name}' in Azure Blob hochgeladen.")

except Exception as ex:
    print("❌ Ausnahme beim Hochladen:")
    print(ex)
    exit(1)
