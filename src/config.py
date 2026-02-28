import os
import dotenv 
dotenv.load_dotenv()
# Connectivity Settings
POLLING_INTERVAL = 5  # Seconds (Heartbeat)

API_KEY = os.getenv("ABUSEIPDB_API_KEY")
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "sentinel.db")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
