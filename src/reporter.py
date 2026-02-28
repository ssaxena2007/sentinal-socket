from src.logger import read_encrypted_logs
import datetime

def generate_report():
    print("="*50)
    print(f"SENTINEL-SOCKET FORENSIC REPORT")
    print(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # This calls your existing decryption logic to print the alerts
    read_encrypted_logs()
    
    print("="*50)
    print("END OF REPORT")

if __name__ == "__main__":
    generate_report()