# Database

## Datenbankstruktur: Vorher-Nachher-Vergleich

### Planung (vorher)

#### User  
• Id (PK), pw (String), username (String), credits (Int), Userart (String), email (String)

#### CheatSheet  
• Id (PK), Title (String), creditCosts (Int), pdf-datei (pdf), prof_id (FK), module_id (FK), user_id (FK), votes (Int)

#### Votes  
• Id (PK), User_Id (FK), CheatSheet_Id (FK), upvotes (Boolean), downvotes (Boolean)

#### Orders  
• Invoicenumber (PK), user_id (FK), creditamount (Int)

#### UnlockedCheatSheet  
• User_Id (FK), Cheatsheet_id (FK)

#### Modules  
• Id (PK), Name (String)

#### Prof  
• Id (PK), Module_ID (FK), Name (String)


### Umsetzung (nachher)

#### user  
• id (PK), email (String), username (String), pw (String), credits (Int), userart (String)

#### cheatsheet  
• id (PK), title (String), description (String), creditcost (Int), pdf_datei (Datei), module (String), professor (String), user_id (FK), votes (Int), created_at (Timestamp)

#### user_cheatsheet_access  
• user_id (FK), cheatsheet_id (FK), vote (Int) // 1 = Upvote, -1 = Downvote, 0 = kein Vote

#### order  
• id (PK), user_id (FK), creditamount (Int)
