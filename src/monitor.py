import psutil
import socket
from src.config import POLLING_INTERVAL

def get_active_connections():
    """Fetches currently established TCP/UDP connections."""
    connections = []
    
    # Iterate through all network connections
    for conn in psutil.net_connections(kind='inet'):
        # We only want connections that are actually 'ESTABLISHED'
        if conn.status == 'ESTABLISHED':
            # remote_address is a tuple (ip, port)
            if conn.raddr:
                remote_ip = conn.raddr.ip
                remote_port = conn.raddr.port
                
                # Try to get the process name associated with this PID
                try:
                    process = psutil.Process(conn.pid)
                    process_name = process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    process_name = "Unknown/System"

                connections.append({
                    "local_ip": conn.laddr.ip,
                    "remote_ip": remote_ip,
                    "remote_port": remote_port,
                    "pid": conn.pid,
                    "process_name": process_name
                })
    return connections

if __name__ == "__main__":
    print("Scanning active connections...")
    conns = get_active_connections()
    for c in conns:
        print(f"[{c['process_name']}] {c['local_ip']} -> {c['remote_ip']}:{c['remote_port']}")