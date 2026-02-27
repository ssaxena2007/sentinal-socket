# Sentinel-Socket

## Current Architecture
- **Monitor (`src/monitor.py`)**: Real-time TCP/UDP polling with Process ID mapping.
- **Data Layer (`src/database.py`)**: SQLite-backed IP reputation management (Whitelist/Blacklist).
- **Secure Logging (`src/logger.py`)**: Fernet-encrypted (Symmetric) forensic log storage.
- **Config Layer (`src/config.py`)**: Centralized path and interval management.

## Security Implementation
- **Data at Rest**: All threat logs are encrypted using a 128-bit Fernet key.
- **Triage**: Tiered analysis using local DB checks and Reverse DNS lookups.