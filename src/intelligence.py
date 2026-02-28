import sqlite3
from datetime import datetime, timedelta
from src.config import DB_PATH, API_KEY
import requests

def get_cached_score(ip):
    """Retrieves score from DB if it's less than 7 days old."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Only select if updated in the last 7 days
        cursor.execute("""
            SELECT score FROM ip_cache 
            WHERE ip_address = ? 
            AND last_updated > datetime('now', '-7 days')
        """, (ip,))
        result = cursor.fetchone()
        return result[0] if result else None

def save_to_cache(ip, score):
    """Saves or updates the IP score in the local cache."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ip_cache (ip_address, score, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(ip_address) DO UPDATE SET
                score=excluded.score,
                last_updated=CURRENT_TIMESTAMP
        """, (ip, score))
        conn.commit()

def check_ip_reputation(ip):
    # 1. Check Cache First
    cached = get_cached_score(ip)
    if cached is not None:
        return cached

    # 2. If not in cache, call API
    if not API_KEY: return None
    
    # ... (Your existing requests.get code here) ...
    
    if response.status_code == 200:
        score = response.json()['data']['abuseConfidenceScore']
        # 3. Save to Cache for next time
        save_to_cache(ip, score)
        return score
    return None