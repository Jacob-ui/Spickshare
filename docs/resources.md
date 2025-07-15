# Dokumentation

## Vorläufige Ressourcen (Gestaltung und Ausarbeitung der Quellen erfolgt später in einem Word-Dokument)

- **12.05.**  
  Besprechung der Idee, Identifikation von Problemen und erste Lösungsansätze.  
  Erstellung und Austausch von Discord-Kanälen sowie gemeinsamer Word-Dateien zur Kommunikation.  
  Ziele für das nächste Treffen besprochen: Einrichtung der Entwicklungsumgebung, GitHub und Informationsbeschaffung zu Python.

- **14.05.**  
  Erfolgreiche Installation und Einrichtung von GitHub sowie Synchronisierung eines gemeinsamen Repositories.  
  Erste Erstellung von Projekten.  
  Als Hilfsmittel dienten unter anderem folgende Videos:  
  - [GitHub Tutorial](https://www.youtube.com/watch?v=0jzjz4MZ4ZU&t=438s)  
  - Für die Datenbankanbindung und besseren Einblick in den Aufbau von Web-Apps wurden weitere Tutorials genutzt:  
    - [Python SQLite Tutorial Deutsch - Web App](https://www.youtube.com/results?search_query=python+sqlite+tutorial+deutsch+web+app)  
    - [SQLite und Flask Tutorial](https://www.youtube.com/watch?v=362fjQdpFlc)  
    - [Generelle Hilfe Flask/Python](https://www.youtube.com/watch?v=gBpiToYbsDM&t)

- **05.06.**  
  Anlegen der Projektdateien.

- **06.06.**  
  Einführung in das Thema Login/Registrierung:  
  - [Flask Login & Registration Tutorial](https://www.youtube.com/watch?v=dam0GPOAvVI)

- **09.06.**  
  Aufgabenaufteilung bis zum 12.06.:  
  - Cooper ergänzt Datenbanken und erstellt Registrierungs- sowie Login-Möglichkeiten.  
  - Jacob ergänzt die Liste mit Spickzettel-Einträgen, fügt einen funktionierenden Upvote/Downvote-Button hinzu und entwickelt bei Zeit eine Sortierfunktion basierend auf Up- und Downvotes.

- **10.06.2025**  
  Tutorials zur Datenbankanbindung und dynamischen Listen:  
  - [Daten aus SQLite mit Python abrufen](https://www.youtube.com/watch?v=Hyo9rIuYlFc)  
  - [Weiteres SQLite Tutorial](https://www.youtube.com/watch?v=KIT4lgR3FWA)  
  - [Dynamic List in Flask](https://www.youtube.com/watch?v=NO-H8z2tV4I)

- **11.06.2025**  
  Anleitung zum Like/Dislike-Button:  
  - [Like/Dislike Button Tutorial](https://www.youtube.com/watch?v=rX7B_SV2EC0)

- **12.06.2025**  
  Weiterentwicklung des Projektes:  
  - Hinzufügen von SQL-Abfragen bei Login/Registrierung.  
  - Anlegen und Teilen der Projektdokumentation.

- **22.06.2025**  
  Weiteres SQLite Tutorial:  
  - [SQLite Tutorial](https://www.youtube.com/watch?v=WBzB7VtH7-g)

- **01.07.2025**  
  Proof File:  
  - [If file proof](https://flask.palletsprojects.com/en/latest/patterns/fileuploads/#handling-uploads)


- **11.07.2025**  
  Account Page and Cheatsheets:  
  - [SQL Alchemy filters](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#simple-equality-filters)
  - [SQL Alchemy func.sum](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.func.sum)

- **14.07.2025**  
  Stripe Integration:
  - [Import Stripe](https://docs.stripe.com/api?lang=python)
  - [Stripe fulfillment](https://docs.stripe.com/checkout/fulfillment)
  - [Stripe Checkout Session](https://docs.stripe.com/api/checkout/sessions/create)
  - [Stripe Method Type](https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-payment_method_types)
  - [Stripe Price data](https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-line_items-price_data)
  - [Stripe Product data](https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-line_items-price_data-product_data)
  - [Stripe Session mode](https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-mode)
  - [Stripe fulfill orders](https://stripe.com/docs/payments/checkout/fulfill-orders)
  - [Stripe cancel url](https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-cancel_url)
  - [Stripe meta data](https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-metadata)
  - [Stripe retrieve](https://stripe.com/docs/api/checkout/sessions/retrieve)



- **24.06.2025**
  An Datenbank weitergearbeitet

- **28.06.2025**
  An Register Funktion weitergearbeitet, teilweise mit claude.ai. Speichert jetzt neue User in der Datanbank:
  - [Bugs fixen] (https://claude.ai/share/644c973d-59db-4614-8e57-cf71e15b4903)

  Implementierung von werkzeug.security, Youtube Tutorial verwendet:
  - [werkzeug.security Tutorial] (https://youtu.be/dam0GPOAvVI?t=5750)

- **29.06.2025**
  Flask_login für Sessions, Authentification und Route Protection implementiert, Youtube Tutorial verwendet:
  - [Flask_login Tutorial] (https://youtu.be/dam0GPOAvVI?t=6589, https://youtu.be/dam0GPOAvVI?t=6355, https://youtu.be/dam0GPOAvVI?t=6715)

- **30.06.2025**
  Wechsel zu SQLAlchemy, teilweise Youtube Tutorial verwendet. Unnötige Dateien wie sql Dateien entfernt:
  - [SQLAlchemy Guide] (https://hwrberlin.github.io/fswd/sqlalchemy.html)
  - [Flask_login UserMixin implementierung] (https://youtu.be/dam0GPOAvVI?t=4993, https://youtu.be/dam0GPOAvVI?t=6784)

- **05.07.2025**
  Download Funktion hinzugefügt, Youtube Tutorial und claude.ai verwendet:
  - [Download Funktion mit BytesIO] (https://youtu.be/pPSZpCVRbvQ?t=322, https://youtu.be/pPSZpCVRbvQ?t=273)
  - [Bug Fixt] (https://claude.ai/share/287d947c-dbf3-4661-9c37-92af1f920cd7)

  Redundante Zeilen entfernt

- **08.07.2025**
  Angefangen, an der Preview Function zu arbeiten, mit Youtube Tutorial:
  - [PyPDF2] (https://youtu.be/OdIHUdQ1-eQ?t=99)

- **09.07.2025**
  Preview Funktion fertig gemacht, Youtube Tutorial und claude.ai verwendet:
  - [PyPDF2] (https://youtu.be/OdIHUdQ1-eQ?t=914)
  - [output.seek Funktion] (https://claude.ai/share/1ed27432-5d2d-4c34-bd75-52f20ac69919 https://docs.python.org/3/library/io.html)
  - [iframe] (https://www.youtube.com/watch?v=aRGdDy18qfY)

  Buy_credits und buy_cheatsheet Funktionen erstellt und vote Funktion verbessert. App.py ein bisschen einheitlicher gemacht

  Has_access Funktionen erstellt, Claude.ai verwendet:
  - [inject_functions] (https://claude.ai/share/882bbdab-e385-445d-a3f9-b3d34192b12e)

  Account Funktion erstellt, Guide verwendet:
  - [SQLAlchemy Inner Join Befehl] (https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_working_with_joins.htm)

- **15.07.2025**
  Flash Message Bug gefixed, claude.ai verwendet:
  - [JS Bundle] (https://getbootstrap.com/docs/5.1/getting-started/introduction/ https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js)
  - [Bug Fix] (https://claude.ai/share/4247021c-b55b-40d8-aefd-1b2ca95f3a8a)

  Design Decisions, Peer Review, Contributions und Resources zu Docs hinzugefügt