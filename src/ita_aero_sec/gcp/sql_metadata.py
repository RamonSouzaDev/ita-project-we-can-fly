import os

try:
    import pymysql
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

class CloudSQLMetadata:
    """Manages identities and tactical metadata leveraging GCP Cloud SQL for fast user validation."""

    def __init__(self, project_id="project-31e1e40c-e499-4462-a66"):
        self.host = os.environ.get("CLOUD_SQL_HOST", "127.0.0.1")
        self.user = os.environ.get("CLOUD_SQL_USER", "tactical_operator")
        self.password = os.environ.get("CLOUD_SQL_PASSWORD", "")
        self.db = os.environ.get("CLOUD_SQL_DATABASE", "wecanfly_metadata")
        self.project_id = project_id

    def connect(self):
        """Establish relational connection."""
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db,
            cursorclass=pymysql.cursors.DictCursor
        )

    def validate_fab_credential(self, user_id, hash_sha256):
        """Validates operator SHA-256 for military level data access (Offloading BigQuery)."""
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT access_level FROM operators WHERE user_id=%s AND credentials_hash=%s"
                cursor.execute(sql, (user_id, hash_sha256))
                result = cursor.fetchone()
                return result is not None
        finally:
            connection.close()
