import psutil
import socket
import sqlite3 # Critical Fix: Standard library import
from src.config import POLLING_INTERVAL, DB_PATH # Critical Fix: Need DB_PATH for triage
from src.logger import log_event_encrypted
from src.intelligence import check_ip_reputation
from src.alerts import send_threat_alert



def get_active_connections():
    """Fetches currently established TCP/UDP connections."""
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED' and conn.raddr:
            try:
                process = psutil.Process(conn.pid)
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown/System"

            connections.append({
                "local_ip": conn.laddr.ip,
                "remote_ip": conn.raddr.ip,
                "remote_port": conn.raddr.port,
                "pid": conn.pid,
                "process_name": process_name
            })
    return connections

def triage_connection(ip):
    """Checks the reputation of an IP and performs reverse DNS."""
    # 1. Reverse DNS
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        hostname = "No Hostname Found"

    # 2. Database Check
    status = "Unknown"
    # Use the DB_PATH we imported from config
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM reputation WHERE ip_address = ?", (ip,))
        result = cursor.fetchone()
        if result:
            status = "Whitelisted" if result[0] == 0 else "Blacklisted"
    
    return status, hostname

if __name__ == "__main__":
    print(f"{'PROCESS':<20} | {'REMOTE IP':<15} | {'HOSTNAME':<25} | {'STATUS'}")
    print("-" * 75)
    
    active_conns = get_active_connections()
    for c in active_conns:
        status, hostname = triage_connection(c['remote_ip'])
        print(f"{c['process_name']:<20} | {c['remote_ip']:<15} | {hostname[:25]:<25} | {status}")
        
        # New Integration Logic
        if status == "Unknown" or status == "Blacklisted":
            log_msg = f"ALERT: {c['process_name']} ({c['pid']}) connected to {c['remote_ip']} ({hostname})"
            log_event_encrypted(log_msg)
        

        status, hostname = triage_connection(c['remote_ip'])

        if status == "Unknown":
            score = check_ip_reputation(c['remote_ip'])


            if score and score > 50:
                send_threat_alert(c['process_name'], c['remote_ip'], score)
                log_msg = f"CRITICAL: High-risk connection ({score}%) from {c['process_name']}"
                log_event_encrypted(log_msg)