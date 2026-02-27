import argparse
import sys
from src.monitor import get_active_connections, triage_connection
from src.logger import read_encrypted_logs, log_event_encrypted
from src.database import init_db

def run_monitor():
    """Starts the heartbeat monitor."""
    print(f"{'PROCESS':<20} | {'REMOTE IP':<15} | {'HOSTNAME':<25} | {'STATUS'}")
    print("-" * 75)
    
    try:
        active_conns = get_active_connections()
        for c in active_conns:
            status, hostname = triage_connection(c['remote_ip'])
            print(f"{c['process_name']:<20} | {c['remote_ip']:<15} | {hostname[:25]:<25} | {status}")
            
            if status == "Unknown" or status == "Blacklisted":
                log_msg = f"ALERT: {c['process_name']} ({c['pid']}) -> {c['remote_ip']} ({hostname})"
                log_event_encrypted(log_msg)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

def main():
    parser = argparse.ArgumentParser(description="Sentinel-Socket: Network Threat Triage Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: start
    subparsers.add_parser("start", help="Start the real-time network monitor")

    # Command: logs
    subparsers.add_parser("logs", help="Decrypt and view the forensic threat logs")

    # Command: init
    subparsers.add_parser("init", help="Initialize the database and directories")

    # Command: allow (Whitelist an IP)
    allow_parser = subparsers.add_parser("allow", help="Whitelist an IP address")
    allow_parser.add_argument("ip", help="The IP address to whitelist")
    allow_parser.add_argument("--desc", default="Manual Whitelist", help="Description for the entry")

    args = parser.parse_args()

    if args.command == "init":
        init_db()
        print("System initialized.")
    elif args.command == "start":
        run_monitor()
    elif args.command == "logs":
        read_encrypted_logs()    
    elif args.command == "allow":
        from src.database import update_reputation
        update_reputation(args.ip, 0, args.desc)
        print(f"IP {args.ip} has been whitelisted.")
    else:
        parser.print_help()
    

if __name__ == "__main__":
    main()