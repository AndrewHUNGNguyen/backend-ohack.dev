import logging
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import sys
import logging
import json

# add logger
logger = logging.getLogger(__name__)
# set logger to standard out
logger.addHandler(logging.StreamHandler())
# set log level
logger.setLevel(logging.INFO)

from datetime import datetime


sys.path.append("../")
load_dotenv()


CDN_SERVER = os.getenv("CDN_SERVER")
GCLOUD_CDN_BUCKET = os.getenv("GCLOUD_CDN_BUCKET")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def upload_to_cdn(directory, source_file_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    gcp_json_credentials_dict = json.loads(GOOGLE_APPLICATION_CREDENTIALS)
    creds = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict)
    project_name = GCLOUD_CDN_BUCKET.split("_")[0]
    storage_client = storage.Client(project=project_name,credentials=creds)
    bucket = storage_client.bucket(GCLOUD_CDN_BUCKET)
    blob = bucket.blob(f"{directory}/{source_file_name}")

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    # generation_match_precondition = 0 # Don't use this because we want to overwrite files

    blob.upload_from_filename(source_file_name)

    logger.info(
        f"File {source_file_name} uploaded to {directory}/{source_file_name}."
    )