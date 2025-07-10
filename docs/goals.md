---
title: Goals
parent: Team Evaluation
nav_order: 1
---

{: .no_toc }
# Goals achieved and missed

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Verbesserung des Vote-Systems

**Goal Definition**  
: Nutzer sollen ein Spickzettel nur einmal bewerten können. Bisher konnte durch wiederholtes Klicken unendlich oft abgestimmt werden.

**Umsetzung**  
: Die Votes wurden mit der Tabelle `user_cheatsheet_access` verknüpft. Jede Bewertung (Upvote/Downvote) wird dort pro User eindeutig gespeichert und mehrfaches Voting verhindert.

---

## Datenbank lauffähig machen

**Goal Definition**  
: Die Datenbank soll initialisiert und vollständig angebunden werden. Login, Registrierung und Datenspeicherung müssen funktionieren.

**Umsetzung**  
: Die Tabellen für User, Cheatsheets, Bestellungen und Zugriff wurden erfolgreich erstellt und verknüpft. Login und Registrierung funktionieren mit Passwort-Hashing, Nutzerrollen und Credits.

---

## Voting mit Datenbank verknüpfen

**Goal Definition**  
: Stimmen für ein Cheatsheet sollen in der Datenbank festgehalten und pro Nutzer nachvollziehbar sein.

**Umsetzung**  
: Votes werden nun über die `user_cheatsheet_access`-Tabelle gespeichert und beim erneuten Aufruf ausgewertet, um Mehrfachabstimmungen zu verhindern.

---

## Upload und Download von PDF-Dateien

**Goal Definition**  
: Registrierte Nutzer sollen PDF-Dateien hochladen und (nach Kauf oder Freischaltung) herunterladen können.

**Umsetzung**  
: Der Upload funktioniert inklusive Beschreibung, Modul und Professorenangabe. Downloads sind nur für freigeschaltete Spickzettel möglich. Die Dateien werden serverseitig gespeichert und sicher zugeordnet.

---

## Vorschau der Spickzettel

**Goal Definition**  
: Vor dem Kauf soll ein Spickzettel teilweise angesehen werden können (z. B. Vorschauseite oder Bild).

**Umsetzung**  
: Eine einfache Vorschaufunktion wurde vorbereitet. Aktuell wird ein Platzhalterbild oder eine reduzierte Seitenversion angezeigt. Weitere Optimierung (automatische Vorschaugenerierung) ist geplant.

---

## Coins (Creditsystem)

**Goal Definition**  
: Nutzer erhalten beim Start kostenlose Coins, um erste Spickzettel testen zu können. Downloads kosten Coins, Uploads bringen keine.

**Umsetzung**  
: Jeder User startet mit einem Coin-Guthaben. Die Preise pro Spickzettel sind einstellbar. Käufe werden in der `order`-Tabelle gespeichert. Coin-Abzüge beim Download sowie spätere Aufladung per Stripe sind vorgesehen.

---

## Coins in der Datenbank verwalten

**Goal Definition**  
: Coins (Credits) sollen in der Datenbank erfasst und korrekt abgerechnet werden (Kauf, Download, Kontostand).

**Umsetzung**  
: Coins sind als Feld `credits` in der `user`-Tabelle hinterlegt. Bei jedem Kauf erfolgt ein Datenbankeintrag in `order` sowie ein Abzug der Coins. Noch offen: Stripe-Integration zur Coin-Aufladung.

# Zusätzlich (Additional)
- Verification with phone number
- Admin Accounts
- Split code into multiple files -> for better readability
- Stripe payment integration



