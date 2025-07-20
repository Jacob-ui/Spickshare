---
title: Improvements
parent: Team Evaluation
nav_order: 2
---

{: .no_toc }
# How we would improve next time

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

# Projekt: Dokumenten-Plattform

## Aktuelle Aufgaben & Verbesserungen

### 1. Votes-System verbessern
- Aktuell können Nutzer unendlich oft auf Vote-Buttons klicken.
- **Ziel:** Pro Nutzer nur eine Stimme (Upvote oder Downvote) erlauben.
- Mehrfachabgaben verhindern, ggf. Speicherung über User-ID / Session.

---

### 2. Datenbank funktionsfähig machen
- Datenbank korrekt initialisieren und mit dem Backend verbinden.
- **Login & Registrierung** über die Datenbank verwalten.
- Alle Benutzerdaten und Dokument-Metadaten dauerhaft speichern.

---

### 3. Account-Seite erstellen
- Persönliche Account-Page für eingeloggte Nutzer implementieren.
- Anzeige von:
  - Hochgeladenen Dokumenten
  - Verbleibenden Credits
  - Benutzerinformationen

---

### 4. Upload-Funktion erweitern
Beim Dokument-Upload folgende Eingabefelder ergänzen:
-  Beschreibung
-  Professorenname
-  Modulname  
Diese Informationen sollen:
- In der Datenbank gespeichert werden
- Auf der Dokument-Detailseite angezeigt werden

---

### 5. PDF-Vorschau verbessern
- Aktuell wird die Vorschau nicht korrekt angezeigt.
- Ziel: Bei z. B. 3-seitigem PDF **nur eine Seite in der Preview** anzeigen.
- Umsetzung über PDF.js oder eine eigene Renderfunktion.

---

### 6. Credit-System & Käufe
- Stripe-Integration zur Abwicklung von Käufen einbinden.
- Gekaufte Credits müssen korrekt:
  - In der Datenbank gespeichert
  - Dem Nutzerkonto zugewiesen werden
- Sicherheitsprüfung & Transaktionslogik erforderlich.

---

### 7. UI verschönern mit Bootstrap
- Sauberes, responsives Layout mit **Bootstrap 5**
- Einheitliche Buttons, Formulare, Navigationsleisten
- Fokus auf gute User Experience

---

### 8. Dokumentation & Quellen überarbeiten
- Projekt-Dokumentation überprüfen & strukturieren
- Alle externen Quellen (z. B. Libraries, Tools) korrekt zitieren
- Sicherstellen, dass README.md und evtl. Wiki vollständig & nachvollziehbar sind

---

### 9. Mehr Nutzerrollen und Rechte
- Unterschiedliche Rollen einführen, z. B. Admins, Moderatoren und normale Nutzer
- So können Admins besondere Bereiche und Funktionen sehen und steuern

---

### 10. Bessere Fehlermeldungen
- Schöne Seiten für Fehler wie „Seite nicht gefunden“ oder „Serverproblem“ machen
- Klare und freundliche Meldungen anzeigen, wenn was schiefgeht
- Fehler im Hintergrund speichern, damit wir sie leichter finden können

