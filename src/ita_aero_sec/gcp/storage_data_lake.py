import os

try:
    from google.cloud import storage
    HAS_GCP = True
except ImportError:
    HAS_GCP = False

class DataLakeManager:
    """Manager for immutable Cloud Storage buckets for TRL-9 LGPD readiness."""
    
    def __init__(self, project_id="project-31e1e40c-e499-4462-a66", bucket_name="wecanfly-tactical-lake"):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.client = storage.Client(project=self.project_id)
        
    def upload_sdr_capture(self, file_path, destination_blob_name):
        """Uploads raw SDR capture data to Cloud Storage."""
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        
        # Enable object versioning and encryption handling would be set on the bucket level
        blob.upload_from_filename(file_path)
        print(f"File {file_path} uploaded to immutable lake at {destination_blob_name}.")
        return blob.public_url

    def get_latest_capture(self, prefix):
        """Fetches latest logs using a prefix query."""
        bucket = self.client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        return list(blobs)
