import os
from azure.storage.blob import BlobServiceClient
import argparse

try:
    print("Azure Blob Storage Python quickstart sample")

    # Argument parser for the connection string
    parser = argparse.ArgumentParser(description='Upload Model')
    parser.add_argument('-c', '--connection', required=True, help="Azure storage connection string")
    args = parser.parse_args()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(args.connection)

    # Container name for your project
    container_name = "bevprogzh-models"  # Your container name in Azure
    model_filename = "region_age_combined_model.pkl"  # Model to upload
    model_directory = r"C:\Users\drito\MDM\bev-prog-zh-v2\model"  # Directory where the model is stored
    local_model_path = os.path.join(model_directory, model_filename)  # Full path to model

    # Check if the container exists, otherwise create it
    container_client = blob_service_client.get_container_client(container_name)

    # If the container doesn't exist, create it
    try:
        container_client.get_container_properties()
        print(f"Container '{container_name}' already exists.")
    except Exception:
        print(f"Container '{container_name}' doesn't exist. Creating container...")
        blob_service_client.create_container(container_name)

    # List blobs in the container and get the existing versions of the model
    blobs = container_client.list_blobs()
    existing_versions = [
        int(blob.name.split("_")[-1].replace(".pkl", ""))  # Get the version number
        for blob in blobs
        if blob.name.startswith("region_age_combined_model") and blob.name.endswith(".pkl")
    ]

    # Calculate the new version number for the model
    new_version = max(existing_versions, default=0) + 1
    print(f"New version of the model will be: {new_version}")

    # Create the new blob name
    new_model_filename = f"region_age_combined_model_{new_version}.pkl"
    print(f"Uploading to Azure Blob Storage as: {new_model_filename}")

    # Create a blob client and upload the model
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=new_model_filename)

    # Upload the model file
    with open(local_model_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"✅ Model '{new_model_filename}' successfully uploaded to '{container_name}'!")

except Exception as ex:
    print('Exception: ')
    print(ex)
    exit(1)
