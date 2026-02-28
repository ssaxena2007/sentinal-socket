# Sentinel-Socket 🛡️

**Network Connection Monitor & Threat Triage Engine**

Sentinel-Socket is a professional-grade security utility designed to monitor active TCP/UDP connections, triage them against global threat intelligence, and maintain an encrypted forensic log of suspicious activity.

## 🚀 Features
- **Real-time Monitoring**: Continuous polling of established connections with PID mapping.
- **Threat Intelligence**: Integrated with AbuseIPDB API for real-time risk scoring.
- **Smart Caching**: SQLite-backed intelligence cache with a 7-day TTL to optimize API usage.
- **Encrypted Forensics**: All suspicious logs are encrypted using 128-bit Fernet (AES).
- **Desktop Alerts**: Native system notifications for high-risk detections (>50% score).
- **Log Rotation**: Automatic archiving of forensic logs to manage disk space.

## 🛠️ Architecture
- **Language**: Python 3.12+
- **Core Libraries**: `psutil`, `cryptography`, `sqlite3`, `requests`, `plyer`.
- **Database**: SQLite (IP Reputation & Intelligence Cache).

## 🔧 Setup
1. **Clone the repo** and initialize a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -r requirements.txt
    
2. **Configure API Key** : Create a .env file in the root and add your AbuseIPDB key:

'''bash
ABUSEIPDB_API_KEY=your_key_here'''

3. **Initialize**: '''bash python main.py init'''



# Sentinel-Socket

## Current Architecture
- **Monitor (`src/monitor.py`)**: Real-time TCP/UDP polling with Process ID mapping.
- **Data Layer (`src/database.py`)**: SQLite-backed IP reputation management (Whitelist/Blacklist).
- **Secure Logging (`src/logger.py`)**: Fernet-encrypted (Symmetric) forensic log storage.
- **Config Layer (`src/config.py`)**: Centralized path and interval management.

## Security Implementation
- **Data at Rest**: All threat logs are encrypted using a 128-bit Fernet key.
- **Triage**: Tiered analysis using local DB checks and Reverse DNS lookups.

## Security & Permissions (Least Privilege)
To operate at full capacity, Sentinel-Socket requires specific permissions:

1. **Network Statistics**: Standard user permissions allow monitoring of the current user's connections.
2. **Process Identification (Admin/Sudo)**: Accessing the `process_name` and `PID` for system-level services (e.g., svchost.exe on Windows or root daemons on Linux) requires Elevated Privileges.
3. **Database & Logs**: The `data/` and `logs/` directories should be restricted to the user running the service to prevent unauthorized access to the `secret.key`.