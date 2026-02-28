import sqlite3
import requests
from datetime import datetime
from src.config import DB_PATH, API_KEY

def get_cached_score(ip):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT score FROM ip_cache 
            WHERE ip_address = ? 
            AND last_updated > datetime('now', '-7 days')
        """, (ip,))
        result = cursor.fetchone()
        return result[0] if result else None

def save_to_cache(ip, score):
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
    # 1. Check Cache
    cached = get_cached_score(ip)
    if cached is not None:
        return cached

    # 2. API Call (Only if not in cache)
    if not API_KEY:
        return None

    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Accept': 'application/json', 'Key': API_KEY}
    params = {'ipAddress': ip, 'maxAgeInDays': '90'}

    try:
        # We assign the result of the request to 'response' here
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            score = response.json()['data']['abuseConfidenceScore']
            save_to_cache(ip, score)
            return score
    except Exception as e:
        print(f"API Error: {e}")
    
    return None