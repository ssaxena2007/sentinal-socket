from plyer import notification

def send_threat_alert(process_name, ip, score):
    """Triggers a native system notification."""
    notification.notify(
        title='⚠️ Sentinel-Socket: Threat Detected',
        message=f'Process: {process_name}\nRemote IP: {ip}\nAbuse Score: {score}%',
        app_name='Sentinel-Socket',
        timeout=10 # Seconds the toast stays visible
    )
