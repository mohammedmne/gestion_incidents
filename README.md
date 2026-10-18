# 🛡️ SOC Platform - Cybersecurity Incident Management

> Final Year Project (PFA) — EMSI Master Cybersecurity 2025-2026  
> ** Mohammed MOUMINE **

---

## 📌 Overview

A full-stack **Security Operations Center (SOC)** platform that combines real-time intrusion detection with a complete incident lifecycle management system. Built as part of our Master's degree in Cybersecurity at EMSI.

The platform consists of two integrated modules:
- **IDS (Intrusion Detection System)** — monitors network traffic using Scapy and automatically creates incidents
- **Web Application** — manages the full incident lifecycle (declaration → qualification → treatment → closure)

---

## 🚀 Features

- 🔍 **Real-time intrusion detection** — port scans, brute force SSH, web scans
- 📊 **Live dashboard** — incident statistics with severity and status tracking
- 🔔 **Automatic alerting** — IDS sends alerts to the Flask API automatically
- 👥 **Role-based access** — Declarant, Analyst, and Admin roles
- 📋 **Audit trail** — timestamped action journal for every incident
- 🔒 **Security headers** — protection against XSS, clickjacking, MIME sniffing
- 🌐 **REST API** — external tools can send alerts via `/api/alerte`

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13 + Flask 3.1 + SQLAlchemy 2.0 |
| IDS | Python + Scapy 2.7 |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Database | SQLite + SQLAlchemy ORM |
| Communication | REST API (JSON) |

---

## 📁 Project Structure

```
gestion_incidents/
├── app/
│   ├── __init__.py          # Flask app factory + security headers
│   ├── models.py            # Database models (Incident, User, Action)
│   ├── routes/
│   │   ├── auth.py          # Login / logout
│   │   └── incidents.py     # Incident CRUD + API endpoint
│   └── templates/
│       ├── base.html
│       ├── auth/login.html
│       └── incidents/
│           ├── dashboard.html
│           ├── detail.html
│           └── nouveau.html
├── ids.py                   # Intrusion Detection System (Scapy)
├── config.py                # App configuration
├── run.py                   # Entry point
└── README.md
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.13+
- Git
- Scapy (requires admin/root privileges)

### Setup

```bash
# Clone the repository
git clone https://github.com/YourUsername/gestion_incidents.git
cd gestion_incidents

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install flask sqlalchemy flask-login scapy requests

# Run the application
python run.py
```

The app will be available at: `http://localhost:5000`

---

## 🔍 Running the IDS

Open a **second terminal** (as Administrator on Windows):

```bash
# Activate venv
venv\Scripts\activate

# Start the IDS (monitors Kali Linux IP by default)
python ids.py
```

The IDS will automatically detect:
- **Port scans** (nmap) → creates a "Scan de ports" incident
- **SSH brute force** (Hydra) → creates a "Brute Force SSH" incident

---

## 🌐 REST API

Send alerts from external tools:

```bash
POST /api/alerte
Content-Type: application/json

{
  "type": "Brute Force SSH",
  "source": "192.168.1.100",
  "gravite": "critique"
}
```

Response:
```json
{
  "status": "ok",
  "incident_id": 10
}
```

---

## 🧪 Security Tests (Chapter 7)

All tests performed in an isolated local lab (Kali Linux VM ↔ Windows host):

| Test | Tool | Result |
|------|------|--------|
| Port Scan | nmap -sS | ✅ Detected & incident created |
| SSH Brute Force | Hydra + rockyou.txt | ✅ Detected & incident created |
| Web Vulnerability Scan | Nikto | ✅ Vulnerabilities found & fixed |
| API Alert Test | curl / PowerShell | ✅ Incident created via REST API |

---

## 🔒 Security Fixes Applied

After Nikto scan detected missing headers, the following were added to all HTTP responses:

```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

---

## 👨‍💻 Authors

| Name | Role |
|------|------|
| Mohammed MOUMINE | Developer & Security Analyst |

**Supervisor:** EMSI Master Cybersecurity  
**Year:** 2025-2026

---

## 📄 License

This project was developed for academic purposes at EMSI (École Supérieure de Management et d'Informatique).
