---
title: Design Decisions
parent: Team Evaluation
nav_order: 3
---

{: .no_toc }
# Design Decisions (chronologisch sortiert)

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

---

## Design Decision 1: Choosing Flask_login over Flask Session for User Authentification and Session Management

### Context  
Wir brauchen eine Authentifizierung, die Login-Zustand über Requests bewahrt und Routen schützt. Anfangs wollten wir Flask `session` manuell nutzen.

### Decision  
Wir entschieden uns für das `flask_login`-Extension.

### Status  
Accepted – 2025-06-29

### Consequences  
+ Vereinfachte Login/Logout und Session-Handling mit Standard-Decorator `@login_required`  
+ Built-in `current_user` Management  
+ Saubere User-Model Anforderungen  
- Erfordert dedizierte User-Klasse und Persistenzsystem  
- Fügt Drittanbieter-Abhängigkeit hinzu

### Alternatives Considered  
**Manuelles Session Handling**  
- Leichtgewichtig, aber fehleranfällig und ohne eingebaute Schutzmechanismen

---

## Design Decision 2: Adopting SQLAlchemy instead of Raw SQL for Database Interaction

### Context  
Bisher Roh-SQL genutzt, aber für `flask_login` brauchen wir eine User-Klasse, was zu SQLAlchemy ORM nahelegt.

### Decision  
Umstieg auf SQLAlchemy ORM.

### Status  
Accepted – 2025-06-29

### Consequences  
+ Klarere, wiederverwendbare Klasse-basierte Modelle  
+ Leichtere Integration mit Flask und `flask_login`  
+ Einfacheres Beziehungsmanagement  
- Bestehenden Code komplett neu schreiben  
- Lernaufwand für ORM  
- Kleine Abstraktionskosten

### Alternatives Considered  
**Raw SQL**  
- Direkt und performant, aber repetitiv und schwieriger wartbar

---

## Designentscheidung 7: Nutzung von Flask-Login’s `@login_required` Dekorator für Schutz wichtiger Routen

### Kontext  
Wichtige Routen wie Credit-Kauf, Cheatsheet-Kauf, Voting und Account-Verwaltung müssen nur für angemeldete Nutzer zugänglich sein.

### Entscheidung  
Wir verwenden Flask-Login’s `@login_required` Dekorator, um Authentifizierung auf diesen Routen sicherzustellen.

### Status  
Akzeptiert – 2025-06-30

### Konsequenzen  
+ Standardisierte und saubere Zugriffskontrolle auf Routenebene  
+ Reduziert Boilerplate-Code dank Wiederverwendung von Flask-Login Features  
+ Gute Integration in Session-Management und Nutzerstatus  
- Kann neue Nutzer frustrieren, wenn Anmeldung als Voraussetzung nicht klar kommuniziert wird

### Alternative Überlegungen  
**Manuelle Authentifizierungsprüfungen in den Funktionen**  
- Vorteile: Volle Kontrolle  
- Nachteile: Fehleranfälliger und weniger wartbar

---

## Design Decision 3: Combining Votes and UserCheatsheetAccess into a single table

### Context  
Getrennte Tabellen für Kaufzugriff und Votes führten zu Redundanz und komplexen Joins.

### Decision  
Zusammenführung in eine Tabelle UserCheatsheetAccess(user_id, cheatsheet_id, vote).

### Status  
Accepted – 2025-07-05

### Consequences  
+ Einfacheres Schema ohne doppelte Foreign Keys  
+ Erzwingt „ein Vote pro User pro Cheatsheet“  
+ Einfachere Abfragen für Zugriff und Vote  
- Tabelle übernimmt zwei Verantwortungen (Zugriff + Voting)  
- Könnte bei Voting-Erweiterungen Refactoring brauchen

### Alternatives Considered  
**Separate Votes-Tabelle**  
- Klare Verantwortlichkeiten, aber komplexere Queries

---

## Designentscheidung 6: Zugriffskontrolle durch Zusammenführen von Cheatsheet-Kauf und Voting in UserCheatsheetAccess

### Kontext  
Nutzer dürfen nur abstimmen, wenn sie Cheatsheet gekauft haben.

### Entscheidung  
Wir prüfen Voting-Berechtigung anhand des Eintrags in UserCheatsheetAccess, der Kauf und Vote speichert.

### Status  
Akzeptiert – 2025-07-06

### Konsequenzen  
+ Einfachere Prüfungen durch eine Tabelle  
+ Verhindert unberechtigte Votes  
+ Atomare Vote-Updates mit Gesamtvotes-Anpassung  
- Komplexere Vote-Updates wegen Differenzen  
- Tabelle hat Doppelverantwortung (Kauf + Voting)

### Alternative Überlegungen  
**Separate Votes-Tabelle**  
- Klare Trennung, aber mehr Joins und Logik

---

## Designentscheidung 9: Nutzung eines Flask Context Processors, um `has_access` in Templates verfügbar zu machen

### Kontext  
Templates brauchen Zugriff auf Funktion, um User-Zugriff auf Cheatsheets zu prüfen.

### Entscheidung  
Funktion `has_access` wird per Context Processor an Templates übergeben.

### Status  
Akzeptiert – 2025-07-06

### Konsequenzen  
+ Kurze, wiederverwendbare Zugriffskontrolle in Templates  
+ Bessere Trennung von Logik und Darstellung  
- Mögliche Performance-Auswirkungen bei vielen Anfragen (evtl. Caching nötig)

### Alternative Überlegungen  
**Explizites Übergeben in Render-Aufrufen**  
- Expliziter, aber mehr Aufwand und Fehleranfälligkeit

---

## Designentscheidung 5: Integration von Stripe Checkout für den Kauf von Credits

### Kontext  
Nutzer sollen Credits sicher und zuverlässig per Kreditkarte kaufen können.

### Entscheidung  
Integration von Stripe Checkout.

### Status  
Akzeptiert – 2025-07-14

### Konsequenzen  
+ PCI-konformer, sicherer Zahlungsablauf mit minimalem Backend-Aufwand  
+ Verwaltung von Zahlungsarten und Sessions über Stripe API  
+ Verknüpfung von Zahlungen mit Nutzer und Credits über Metadata  
- Drittanbieter-Abhängigkeit und sichere API-Schlüssel-Verwaltung nötig  
- Zahlungsbestätigung muss sicher (auch asynchron) erfolgen  
- Abhängigkeit vom externen Dienst mit Ausfallrisiko

### Alternative Überlegungen  
**Manuelles Creditsystem ohne Zahlung**  
- Einfach, aber kein Umsatz und unsicher  
**Andere Payment-Provider**  
- Unterschiedliche Gebühren und Features, aber aufwendiger

---

## Designentscheidung 8: Rollenbasierte Zugriffskontrolle mittels eigenem `admin_required` Dekorator

### Kontext  
Admin-Funktionen sollen nur für Admins zugänglich sein.

### Entscheidung  
Eigenen `admin_required` Decorator erstellt, der Rolle prüft.

### Status  
Akzeptiert – 2025-07-16

### Konsequenzen  
+ Einfache und zentrale Zugriffskontrolle für Admins  
+ Wiederverwendbar und erweiterbar  
- Rollenmanagement muss gepflegt werden  
- Keine fein granulare Berechtigungssteuerung

### Alternative Überlegungen  
**RBAC-Bibliotheken wie Flask-Principal**  
- Mehr Flexibilität, aber komplexer

---

## Design Decision 4: Using Email Verification with itsdangerous and flask_mail Instead of Phone Verification with Firebase

### Context  
User-Verifikation sollte ohne JS oder externe Programme funktionieren, Firebase Telefon-Verifikation passt nicht.

### Decision  
Implementierung der Email-Verifikation via itsdangerous und flask_mail.

### Status  
Accepted – 2025-07-18

### Consequences  
+ Kompatibel mit Projektrestriktionen, komplett in Python  
+ Einfache Integration in Flask und User-Modell  
+ Kostenlos bei niedrigem Versandvolumen  
- Weniger sicher als Telefon-Verifikation (Email-Spoofing möglich)  
- Nutzer können Fake/Temporäre Emails nutzen  
- E-Mail Versand und Token-Verwaltung müssen manuell gehandhabt werden

### Alternatives Considered  
**Phone Verification mit Firebase**  
- Sicherer, aber nicht kompatibel mit Projektanforderungen, komplexer

---
