import os
from azure.storage.blob import BlobServiceClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure Blob Storage connection string
connect_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Directory where trained models are stored
model_directory = "model_trained"  # This is where your models will be stored
container_name = "bevprogzh-models"

# Function to upload the model to Azure Blob Storage
def upload_model(model_filename):
    logger.info(f"🔍 Checking if the file '{model_filename}' exists...")

    if not os.path.exists(model_filename):
        logger.error(f"❌ The file '{model_filename}' was not found. Ensure the model is saved.")
        raise FileNotFoundError(f"The file '{model_filename}' was not found.")

    # Attempt to create the container (will fail if already exists)
    try:
        blob_service_client.create_container(container_name)
        logger.info(f"✅ Container '{container_name}' created.")
    except Exception:
        logger.info(f"ℹ️ Container '{container_name}' already exists.")

    # List all blobs in the container and get the existing versions of the model
    blobs = blob_service_client.get_container_client(container_name).list_blobs()
    existing_versions = [
        int(blob.name.split("-")[-1].replace(".pkl", "")) 
        for blob in blobs 
        if blob.name.startswith("region_age_combined_model") and blob.name.endswith(".pkl")
    ]
    
    # Calculate the new version of the model
    new_version = max(existing_versions, default=0) + 1
    logger.info(f"✅ New model version will be: {new_version}")

    # Upload the new model to Azure Blob Storage with versioning
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=f"region_age_combined_model_v{new_version}.pkl"
    )
    
    with open(model_filename, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    logger.info(f"✅ Model uploaded as version {new_version} to Azure Blob Storage!")

# Example usage:
if __name__ == "__main__":
    # Assuming your combined model is saved in the 'model_trained' directory
    model_filename = os.path.join(model_directory, "region_age_combined_model.pkl")
    upload_model(model_filename)
