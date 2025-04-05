import os
from azure.storage.blob import BlobServiceClient
import argparse

# Anpassungen:
# - Die Umgebungsvariable 'AZURE_STORAGE_CONNECTION_STRING' wird verwendet, um die Verbindung zu Azure herzustellen.
# - Der Blob-Containername und die Modell-Datei wurden auf dein Projekt angepasst.

try:
    print("Azure Blob Storage Python quickstart sample")

    # Parser für die Kommandozeilenargumente
    parser = argparse.ArgumentParser(description='Upload Model')
    parser.add_argument('-c', '--connection', required=True, help="Azure Storage Connection String")
    args = parser.parse_args()

    # Azure Blob Service Client erstellen
    blob_service_client = BlobServiceClient.from_connection_string(args.connection)

    # Container-Name für das Modell festlegen
    container_name = "bevprogzh-models"  # Der Name des Containers in Azure Blob Storage
    model_filename = "region_age_combined_model.pkl"  # Das Modell, das hochgeladen werden soll

    # Überprüfen, ob der Container bereits existiert, ansonsten erstellen
    container_client = blob_service_client.get_container_client(container_name)

    # Wenn der Container nicht existiert, wird er erstellt
    try:
        container_client.get_container_properties()
        print(f"Container '{container_name}' existiert bereits.")
    except Exception as e:
        print(f"Container '{container_name}' existiert nicht. Erstelle Container...")
        blob_service_client.create_container(container_name)

    # Listet alle Blobs im Container und ermittelt die höchste Version des Modells
    blobs = container_client.list_blobs()
    existing_versions = [
        int(blob.name.split("-")[-1].replace(".pkl", ""))  # Holt die Versionsnummer aus dem Dateinamen
        for blob in blobs
        if blob.name.startswith("region_age_combined_model") and blob.name.endswith(".pkl")
    ]
    
    # Berechnet die neue Versionsnummer
    new_version = max(existing_versions, default=0) + 1
    print(f"Neue Modellversion wird: v{new_version}")

    # Blob-Client erstellen und das Modell hochladen
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"region_age_combined_model_v{new_version}.pkl")
    print(f"Uploading '{model_filename}' as version v{new_version} to Azure Blob Storage...")

    # Modell-Datei hochladen
    local_model_path = os.path.join("model", model_filename)  # Pfad zum Modell im lokalen Verzeichnis
    with open(local_model_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)  # Modell hochladen und überschreiben, falls es bereits existiert

    print(f"✅ Modell '{model_filename}' erfolgreich als Version v{new_version} in den Container '{container_name}' hochgeladen!")

except Exception as ex:
    print('Exception: ')
    print(ex)
    exit(1)
