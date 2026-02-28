import requests
from src.config import API_KEY

def check_ip_reputation(ip):
    """Fetches the abuse confidence score from AbuseIPDB."""
    if not API_KEY:
        return None  # Skip if no key is configured

    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['data']['abuseConfidenceScore']
    except Exception as e:
        print(f"Intelligence Error: {e}")
    
    return None