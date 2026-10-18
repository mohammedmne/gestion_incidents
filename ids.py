from scapy.all import sniff, IP, TCP
import requests
from collections import defaultdict

connection_count = defaultdict(int)
alerted = set()

API_URL = "http://localhost:5000/api/alerte"

# ← Seule IP autorisée à déclencher des alertes
KALI_IP = "172.30.0.153"

def detect(packet):
    if IP not in packet or TCP not in packet:
        return

    src = packet[IP].src
    
    # Ignore tout sauf Kali
    if src != KALI_IP:
        return

    dst_port = packet[TCP].dport
    connection_count[src] += 1

    # Scan de ports
    if connection_count[src] > 10 and src not in alerted:
        alerted.add(src)
        requests.post(API_URL, json={
            "type": "Scan de ports nmap",
            "source": src,
            "gravite": "haute"
        })
        print(f"[IDS] Scan détecté depuis {src}")

    # Brute Force SSH
    if dst_port == 22 and (src, 22) not in alerted:
        alerted.add((src, 22))
        requests.post(API_URL, json={
            "type": "Brute Force SSH",
            "source": src,
            "gravite": "critique"
        })
        print(f"[IDS] Brute Force SSH détecté depuis {src}")

print("[IDS] Surveillance active - En attente de Kali (172.30.0.153)...")
sniff(filter=f"tcp and src host {KALI_IP}", prn=detect, store=False)