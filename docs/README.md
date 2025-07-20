# Cheatsheet Sharing Website

Diese Webanwendung ermöglicht den Kauf und Zugriff auf Cheatsheets sowie Benutzer-Registrierung, E-Mail-Verifizierung, Zahlungsabwicklung via Stripe und Voting-Funktion.

---

## Features

- Benutzer-Registrierung und Login
- Kauf von Credits via Stripe
- Cheatsheets kaufen und verwalten
- Voting für Cheatsheets
- E-Mail-Verifizierung
- Admin-Bereich für Cheatsheet-Management

---

## Voraussetzungen

- Python 3.8 oder höher
- Virtuelle Umgebung (empfohlen)
- Stripe API Key (für Zahlungsabwicklung)
- Mailserver-Zugang (z.B. Gmail SMTP) für E-Mail-Verifikation

---

## Installation

1. **Repository klonen:**

```bash
git clone https://github.com/dhttps://github.com/Jacob-ui/Spickshare.git
cd dein-repo
```

```bash
python -m venv .venv
source .venv/bin/activate
.venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Falls du **keine `requirements.txt`** hast, installiere manuell:

```bash
pip install Flask Flask-SQLAlchemy Flask-Login PyPDF2 stripe itsdangerous Flask-Mail
```

---
## Verwendete Technologien

| Technologie     | Beschreibung                            |
|----------------|------------------------------------------|
| Flask           | Webframework                            |
| SQLAlchemy      | ORM für die Datenbank                   |
| Flask-Login     | Login & User-Management                 |
| Flask-Mail      | E-Mail-Verifikation                     |
| PyPDF2          | PDF-Verarbeitung                        |
| Stripe API      | Bezahlfunktion mit Checkout             |
| itsdangerous    | Token-Erstellung für Verifikation       |

pip install Flask Flask-SQLAlchemy Flask-Login PyPDF2 stripe itsdangerous Flask-Mail
