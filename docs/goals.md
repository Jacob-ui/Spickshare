---

## Benutzerrollen: Admin & Verifiziert

**Goal Definition**  
: Verschiedene Nutzerrollen sollen unterschiedliche Rechte erhalten – z. B. Admins für Management-Funktionen, verifizierte Nutzer mit mehr Vertrauen.

**Umsetzung**  
: Die Rolle wird in der Spalte `userart` gespeichert (`admin`, `verified`, `not verified`). Admins haben Zugriff auf besondere Seiten wie `/all-cheatsheets/`. Verifizierte Nutzer erhalten Bonus-Credits und sind für weitere Features vorgesehen.

---

## E-Mail-Versand einrichten

**Goal Definition**  
: Die Plattform soll in der Lage sein, automatisierte E-Mails zu verschicken (z. B. Verifizierungs-Links).

**Umsetzung**  
: Integration von `Flask-Mail` mit SMTP-Zugang über Gmail. Die Konfiguration ist im Code hinterlegt (für Testumgebung fest verdrahtet). Die E-Mail enthält personalisierten Text und einen Token-Link zur Verifizierung.

---

## Vorbelegung der Datenbank (Insert Sample Data)

**Goal Definition**  
: Beim Starten der Anwendung soll es möglich sein, Testdaten für Nutzer zu generieren.

**Umsetzung**  
: Über den Endpunkt `/insert/sample` werden zwei Admin-Nutzer in die Datenbank geschrieben – mit Passwort-Hashing und Startguthaben. Dies vereinfacht die Entwicklungs- und Testphase.

---

## Trennung von Upload und Zugriff (Access Control)

**Goal Definition**  
: Nur Nutzer mit gültigem Zugriff sollen Dateien herunterladen oder bewerten können.

**Umsetzung**  
: Beim Download und Voting wird geprüft, ob der User das Cheatsheet gekauft hat. Ohne Kauf ist weder Download noch Voting möglich. Zugriff wird über die Tabelle `user_cheatsheet_access` geprüft.

---

## Flash-Nachrichten für Nutzerfeedback

**Goal Definition**  
: Nutzer sollen direkt Rückmeldung zu Aktionen (Erfolg, Fehler, Warnungen) erhalten.

**Umsetzung**  
: Über Flask `flash()` werden Statusnachrichten erzeugt. Sie erscheinen bei Registrierung, Login, Upload, Voting, Käufen etc. Nachrichten sind nach Typen (success, error, danger) gegliedert.

---

## PDF-Dateien sicher verarbeiten

**Goal Definition**  
: Es dürfen nur gültige PDF-Dateien hochgeladen und verarbeitet werden.

**Umsetzung**  
: Überprüfung der Dateiendung `.pdf`, Lesen über `PyPDF2`, Extraktion der ersten Seite für Vorschau. Beim Upload wird die Datei als `Bytes` gespeichert und direkt in der Datenbank hinterlegt.

---

## Sicherer Login mit Passwort-Hashing

**Goal Definition**  
: Passwörter dürfen nicht im Klartext gespeichert werden.

**Umsetzung**  
: Alle Passwörter werden beim Registrieren mit `werkzeug.security.generate_password_hash()` verschlüsselt. Beim Login erfolgt ein Abgleich mit `check_password_hash()`.

---

## Trennung von GET- und POST-Requests

**Goal Definition**  
: Logik für Formularanzeige und -verarbeitung soll sauber getrennt werden.

**Umsetzung**  
: Bei Registrierung, Login, Upload etc. wird zwischen `GET` (Formular anzeigen) und `POST` (Daten verarbeiten) unterschieden. Fehlerbehandlung erfolgt jeweils im `POST`.

---

## Modulare Strukturierung mit Models

**Goal Definition**  
: Die Datenbank-Modelle sollen ausgelagert und übersichtlich strukturiert sein.

**Umsetzung**  
: Das Modell `User`, `Cheatsheet`, `UserCheatsheetAccess` wurde in ein separates Modul (`models.py`) ausgelagert. Damit bleibt die Hauptdatei schlank und besser wartbar.

---

## Schutz vor doppeltem Kauf

**Goal Definition**  
: Ein Nutzer soll ein Cheatsheet nicht mehrfach kaufen können.

**Umsetzung**  
: Vor jedem Kauf wird geprüft, ob bereits ein Eintrag in `user_cheatsheet_access` existiert. Falls ja, wird der Kauf unterbunden und eine Warnung angezeigt.

---

## Zugriffsschutz auf Admin-Seiten

**Goal Definition**  
: Nur Admins sollen Zugang zu bestimmten Funktionen und Seiten haben.

**Umsetzung**  
: Mit dem Decorator `@admin_required` wird geprüft, ob der aktuelle Nutzer eingeloggt und als `admin` gekennzeichnet ist. Sonst wird zur Startseite weitergeleitet.

---

## Datenbankstruktur automatisch initialisieren

**Goal Definition**  
: Die Datenbanktabellen sollen bei Serverstart automatisch angelegt werden, wenn sie nicht existieren.

**Umsetzung**  
: Beim Start der Flask-App wird innerhalb des `if __name__ == "__main__"`-Blocks `db.create_all()` ausgeführt. So wird die Datenbank bei Erststart erstellt.

---
