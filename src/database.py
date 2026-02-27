import sqlite3
from src.config import DB_PATH

def init_db():
    """Initializes the database and creates the necessary tables."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Table for IP Reputation (0 = Whitelist, 1 = Blacklist)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reputation (
                ip_address TEXT PRIMARY KEY,
                status INTEGER NOT NULL,
                description TEXT
            )
        ''')
        
        # Table for Connection Logs (Raw history for forensics)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connection_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                local_address TEXT,
                remote_address TEXT,
                status TEXT,
                pid INTEGER,
                process_name TEXT
            )
        ''')
        conn.commit()

if __name__ == "__main__":
    # Test initialization
    init_db()
    print(f"Database initialized at {DB_PATH}")