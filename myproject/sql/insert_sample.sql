BEGIN TRANSACTION;
DELETE from users;
DELETE from modules;
DELETE from profs;
DELETE from cheatsheets;
DELETE from votes;
DELETE from orders;
DELETE from unlocked_cheatsheet;
INSERT INTO users (username, pw, credits, userart, email) VALUES ("Cooper","Cooper1", 100, "admin", "s_woolley23@stud.hwr-berlin.de");
INSERT INTO users (username, pw, credits, userart, email) VALUES ("Jacob","Jacob1", 100, "admin", "s_gotter23@stud.hwr-berlin.de");
INSERT INTO modules (name) VALUES ("OOP2");
INSERT INTO profs (modules_id, name) VALUES (1, "Schaal");
INSERT INTO cheatsheets (title, creditcost, pdf_datei, modules_id, profs_id, users_id, votes) VALUES ("Demo", 2, "Demo", 1, 1, 1, 200);
INSERT INTO cheatsheets (title, creditcost, pdf_datei, modules_id, profs_id, users_id, votes) VALUES ("Demo2", 3, "Demo2",1, 1, 2, 200);
INSERT INTO votes (users_id, cheatsheets_id, upvote) VALUES (1, 1, 1);
INSERT INTO orders (users_id, creditamount) VALUES (1, 2);
INSERT INTO unlocked_cheatsheet (users_id, cheatsheets_id) VALUES (2, 1);
INSERT INTO unlocked_cheatsheet (users_id, cheatsheets_id) VALUES (1, 2);
COMMIT;
