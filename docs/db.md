# Database

### User
•	Id (PK), pw (String), username (String), credits (Int), Userart(String), email(String)

### CheatSheet
•	Id (PK), Title (String), creditCosts (Int), pdf-datei (pdf), prof_id (FK), module_id (FK), user_id (FK), votes (Int)

### Votes
•	Id (PK), User_Id (FK), CheatSheet_Id (FK), upvotes (Boolean), downvotes (Boolean)

### Orders
•	Invoicenumber (PK), user_id (FK),  creditamount (int)

### UnlockedCheatSheet
•	User_Id (FK), Cheatsheet_id (FK)

### Modules
•	Id (PK), Name (String)

### Prof
•	Id (PK), Module_ID (FK), Name (String)