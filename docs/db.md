---
title: Database
parent: Team Evaluation
nav_order: 6
---

{: .no_toc }
# Database (vorher und nachher)

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

---

# Database

## Datenbankstruktur: Vorher-Nachher-Vergleich

### Planung (vorher)

#### User  
• id (PK), pw (String), username (String), credits (Int), userart (String), email (String)

#### CheatSheet  
• id (PK), title (String), creditCosts (Int), pdf_datei (pdf), prof_id (FK), module_id (FK), user_id (FK), votes (Int)

#### Votes  
• id (PK), user_id (FK), cheatsheet_id (FK), upvotes (Boolean), downvotes (Boolean)

#### Orders  
• invoicenumber (PK), user_id (FK), creditamount (Int)

#### UnlockedCheatSheet  
• user_id (FK), cheatsheet_id (FK)

#### Modules  
• id (PK), name (String)

#### Prof  
• id (PK), module_id (FK), name (String)

---

### Umsetzung (nachher)

#### user  
• `id` (PK)  
• `email` (String, unique, not null)  
• `username` (String, unique, not null)  
• `pw` (String, not null)  
• `credits` (Int, default = 0)  
• `userart` (String, default = "not verified")  

#### cheatsheet  
• `id` (PK)  
• `title` (String, not null)  
• `description` (String, not null)  
• `courseOfStudy` (String, not null)  
• `creditcost` (Int, default = 1)  
• `pdf_datei` (Binary, not null)  
• `module` (String, not null)  
• `professor` (String, not null)  
• `user_id` (FK to user.id, nullable)  
• `votes` (Int, default = 0)  
• `created_at` (Timestamp, default = current time)  

#### user_cheatsheet_access  
• `user_id` (FK to user.id, PK)  
• `cheatsheet_id` (FK to cheatsheet.id, PK)  
• `vote` (Int, default = 0)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 1 = Upvote, -1 = Downvote, 0 = Kein Vote  

#### order  
• `id` (PK)  
• `user_id` (FK to user.id)  
• `creditamount` (Int)

---

> **Hinweis zu Modulen & Professoren:**  
> Ursprünglich geplante Tabellen `Module` und `Professor` wurden nicht implementiert. Stattdessen werden `module` und `professor` direkt als Strings im Cheatsheet gespeichert. Dies reduziert Komplexität, verhindert jedoch relationale Integrität.
