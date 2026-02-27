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