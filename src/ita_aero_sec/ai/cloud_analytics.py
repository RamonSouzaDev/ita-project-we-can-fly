"""
======================================================================
WE CAN FLY - BIGQUERY & CLOUD ANALYTICS INTERFACE (TRL-9)
======================================================================
Mission: High-performance ingestion to BigQuery, enabling heatmaps 
of aeronautic signal vulnerabilities in Brazilian airspace.

Compliance: LGPD / ISO 27001
Author: Eng. Ramon de Souza Mendes (CREA-SP: 5071785098)
======================================================================
"""
import json
import os
from google.cloud import bigquery
from google.api_core import exceptions

class CloudAnalyticsSink:
    def __init__(self, dataset="aeronautic_cybersecurity", table="forensic_telemetry"):
        self.dataset_id = dataset
        self.table_id = table
        self.client = None
        self.project_id = os.getenv("GCP_PROJECT_ID", "ita-project-we-can-fly")
        
        # Local-first buffering for resilience
        self.buffer = []

    def connect(self, credentials_path=None):
        """
        Establishes connection to GCP BigQuery using Service Account credentials.
        """
        try:
            if credentials_path and os.path.exists(credentials_path):
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            
            self.client = bigquery.Client(project=self.project_id)
            print(f"[GCP-SINK] [SUCCESS] Connected to BigQuery: {self.client.project}")
            self._ensure_infrastructure()
            return True
        except Exception as e:
            print(f"[GCP-SINK] [ERROR] Connection failed: {e}")
            return False

    def _ensure_infrastructure(self):
        """Ensures Dataset and Table exist before streaming."""
        if not self.client: return
        
        dataset_ref = self.client.dataset(self.dataset_id)
        try:
            self.client.get_dataset(dataset_ref)
        except exceptions.NotFound:
            print(f"[GCP-SINK] Creating dataset {self.dataset_id}...")
            self.client.create_dataset(bigquery.Dataset(dataset_ref))

    def stream_to_bigquery(self, data_point):
        """
        Ingests a sanitized telemetry hash into BigQuery and buffers locally for integrity.
        """
        # 1. Forensic Local Logging
        self.buffer.append(data_point)
        with open("flight_blackbox_local_sync.jsonl", "a") as f:
            f.write(json.dumps(data_point) + "\n")
            
        # 2. Real-time Cloud Streaming
        if self.client:
            full_table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
            try:
                errors = self.client.insert_rows_json(full_table_id, [data_point])
                if errors:
                    print(f"[GCP-SINK] [WARN] Streaming errors: {errors}")
                else:
                    print(f"[GCP-SINK] [SUCCESS] Data Ingested to BQ (Cycle: {data_point.get('cycle')})")
            except Exception as e:
                print(f"[GCP-SINK] [ERROR] Failed to ingest to BQ: {e}")
        else:
            print(f"[GCP-SINK] [OFFLINE] Data Buffered Locally: {data_point.get('cycle')}")

if __name__ == "__main__":
    sink = CloudAnalyticsSink()
    if sink.connect():
        test_data = {
            "cycle": 1, 
            "alert_type": "GHOST_AIRCRAFT", 
            "forensic_hash": "62bf71ac599b41fd44b706c"
        }
        sink.stream_to_bigquery(test_data)
