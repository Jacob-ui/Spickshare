import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash #https://youtu.be/dam0GPOAvVI?t=5750
from flask_login import LoginManager, login_user, login_required, logout_user, current_user #https://youtu.be/dam0GPOAvVI?t=6589
from models import User, db, Cheatsheet, UserCheatsheetAccess
from io import BytesIO #https://youtu.be/pPSZpCVRbvQ?t=322
import PyPDF2 as pdf #https://youtu.be/OdIHUdQ1-eQ?t=99

app = Flask(__name__, instance_relative_config=True) #https://claude.ai/share/644c973d-59db-4614-8e57-cf71e15b4903 to fix multiple instance folder bug


# Konfiguration
app.instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance") #https://claude.ai/share/644c973d-59db-4614-8e57-cf71e15b4903 to fix multiple instance folder bug

app.config.from_mapping(
    SECRET_KEY="secret_key_just_for_dev_environment",
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, "spickshare.db")}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False 
)

#Schauen ob DB existiert
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# DB initialisieren
db.init_app(app)

login_manager = LoginManager() #https://youtu.be/dam0GPOAvVI?t=6784
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

print("Instance path:", app.instance_path)
print("Database path:", app.config["SQLALCHEMY_DATABASE_URI"])

# Startseite
@app.route("/")
def start():
    return redirect(url_for("index"))

@app.route("/index/")
def index():
    cheatsheets = Cheatsheet.query.order_by(Cheatsheet.votes.desc()).all()  #https://www.youtube.com/watch?v=0_AoM58PSlA  
    return render_template("index.html", cheatsheets=cheatsheets, user=current_user) #https://youtu.be/dam0GPOAvVI?t=7011

#Login:
@app.route("/login/", methods=["GET", "POST"]) #https://youtu.be/dam0GPOAvVI?t=3449 für die GET und POST Teile des Codes
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pw = request.form.get("password")

        if not username or not pw:#Fehlermeldung mit Flash
            flash("Please fill out both fields!")
        else:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.pw, pw):
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("Username or password incorrect!")

    return render_template("login.html")


# Registrierung:
@app.route("/register/", methods=["GET", "POST"]) #
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        pw = request.form.get("password")
        pw2 = request.form.get("password2")


        if not email or not username or not pw or not pw2:
            flash("Bitte fülle alle Felder aus.")
        elif pw != pw2:
            flash("Passwörter stimmen nicht überein!")
        else:
            try: 
                user_exists = User.query.filter(
                    (User.username == username) | (User.email == email)
                ).first()
                if user_exists:
                    flash("Benutzername oder E-Mail existiert bereits.")#Fehlermeldung
                else:
                    new_user = User(
                        username=username,
                        pw=generate_password_hash(pw),
                        email=email,
                        credits=0,
                        userart="not verified"
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    
                    flash("Registrierung erfolgreich! Bitte einloggen.", "success")#Flash Nachrichten zum erfolgreichen Login
                    return redirect(url_for("login"))
            except Exception as e:
                db.session.rollback()
                flash(f"Database error: {str(e)}")

    return render_template("register.html")

@app.route("/logout")
@login_required #https://youtu.be/dam0GPOAvVI?t=6715
def logout():
    logout_user()
    return redirect(url_for("index"))

    
#upload cheatsheets with html input https://www.youtube.com/watch?v=GQLRVhXnZkE&t=127s bis 4:40 und https://www.youtube.com/watch?v=pPSZpCVRbvQ gesamt
@app.route("/upload/", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        # Nur das Uploadformular anzeigen
        return render_template("upload.html")

    # POST: Daten verarbeiten
    title = request.form.get("title")
    description = request.form.get("description")
    file = request.files.get("file")
    module = request.form.get("module")
    professor = request.form.get("professor")



    if not file or file.filename == "":#Fehler abfangen und mit flash ausgeben
        flash("Keine Datei ausgewählt!")
        return redirect(url_for("upload"))

    if not title:
        flash("Titel darf nicht leer sein.")
        return redirect(url_for("upload"))
    
    if not module:
        flash("Modul darf nicht leer sein.")
        return redirect(url_for("upload"))
    
    if not professor:
        flash("Professor darf nicht leer sein.")
        return redirect(url_for("upload"))

    if not description:
        flash("Beschreibung darf nicht leer sein.")
        return redirect(url_for("upload"))
    
    if not file.filename.lower().endswith(".pdf"):
        flash("Nur PDF-Dateien sind erlaubt.")
        return redirect(url_for("upload"))

    try: #from Eingaben in neuem Cheatsheet objekt speichern
        new_sheet = Cheatsheet(
            title=title,
            description=description,
            pdf_datei=file.read(),
            user_id=current_user.id,
            professor=professor,
            module=module,
        )
        db.session.add(new_sheet)
        db.session.commit()

        flash(f"Upload erfolgreich: {file.filename}", "success")
        return redirect(url_for("index"))

    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Hochladen: {str(e)}")
        return redirect(url_for("upload"))

# Download Cheetsheet
@app.route("/download/<int:cheatsheet_id>", methods=["GET"]) #https://youtu.be/pPSZpCVRbvQ?t=273
@login_required
def download(cheatsheet_id):
    cheatsheet = Cheatsheet.query.filter_by(id=cheatsheet_id).first()

    if not cheatsheet:
        flash("Cheatsheet nicht gefunden!")
        return redirect(url_for("index"))
    

    return send_file(BytesIO(cheatsheet.pdf_datei), 
                     download_name = f"{cheatsheet.title}.pdf", #https://claude.ai/share/287d947c-dbf3-4661-9c37-92af1f920cd7 bug fix
                     as_attachment = True,
                     mimetype = "application/pdf") #https://claude.ai/share/287d947c-dbf3-4661-9c37-92af1f920cd7 macht code sicherer

@app.route("/preview/<int:cheatsheet_id>",methods=["GET"]) #https://youtu.be/OdIHUdQ1-eQ?t=914 teilweise hiermit gemacht
def preview(cheatsheet_id):
    cheatsheet = Cheatsheet.query.filter_by(id=cheatsheet_id).first()

    if not cheatsheet:
        flash("Cheatsheet nicht gefunden!")
        return redirect(url_for("index"))
    
    try:
        pdf_reader = pdf.PdfReader(BytesIO(cheatsheet.pdf_datei))
        pdf_writer = pdf.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[0])

        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0) #https://claude.ai/share/1ed27432-5d2d-4c34-bd75-52f20ac69919 https://docs.python.org/3/library/io.html Ändert Stream Position wieder zum Anfang

        return send_file(
            output,
            download_name=f"{cheatsheet.title}_preview.pdf",
            mimetype="application/pdf",
            as_attachment=False,
        )

    except Exception as e:
        flash(f"Fehler beim Erstellen der Vorschau: {str(e)}")
        return redirect(url_for("index"))


#Credits kaufen
@app.route("/buy-credits", methods=["GET", "POST"])
@login_required
def buy_credits():
    if request.method == 'POST':
        quantity = request.form.get("quantity")
    
        try:

            if not quantity:
                flash("Please enter a quantity!")
            
            elif not quantity.isnumeric():
                flash("Please enter a number")

            elif int(quantity) <= 0:
                flash("Please enter a number greater than zero.")
            
            else:
                current_user.credits += int(quantity)
                db.session.commit()
                flash("Purchase successful!", "success")
                return redirect(url_for("index"))
        except Exception as e:
                    db.session.rollback()
                    flash(f"Database error: {str(e)}")

    return render_template("buy-credits.html")

@app.route("/buy-cheatsheet", methods=["POST"])
@login_required
def buy_cheatsheet():
    cheatsheet_id = request.form.get("id")
    cheatsheet = Cheatsheet.query.get(cheatsheet_id)
    access = UserCheatsheetAccess.query.filter_by(
        user_id = current_user.id,
        cheatsheet_id = cheatsheet_id
    ).first()
    
    try: 
        if not cheatsheet:  #Fehler abfangen und mit flash ausgeben
            flash("Cheatsheet nicht gefunden.")
            return redirect(url_for("index"))
        
        elif current_user.credits < cheatsheet.creditcost:
            flash("Please buy sufficient credits!")
        
        elif access:
            flash("You already own this cheatsheet.")

        else:
            current_user.credits -= cheatsheet.creditcost

            new_access = UserCheatsheetAccess(
                user_id = current_user.id,
                cheatsheet_id = cheatsheet_id
            )

            db.session.add(new_access)
            db.session.commit()
            flash("Purchase successful!", "success")
        
    except Exception as e:
            db.session.rollback()
            flash(f"Database error: {str(e)}")

    return redirect(url_for("index"))

# Voting +/-
@app.route("/vote", methods=["POST"])
@login_required
def vote():
    cheatsheet_id = request.form.get("id") # fragt id vom sheet an
    vote_input = request.form.get("Voteinput") # liest aus index den +/- Button aus
    cheatsheet = Cheatsheet.query.get(cheatsheet_id)
    access = UserCheatsheetAccess.query.filter_by(
        user_id = current_user.id,
        cheatsheet_id = cheatsheet_id
    ).first()
    vote_value = 1 if vote_input =="+" else -1 if vote_input =="-" else 0

    
    if not cheatsheet: #Fehler abfangen und mit flash ausgeben
        flash("Cheatsheet nicht gefunden.","error")
        return redirect(url_for("index"))

    try:
        if access:
            differenz = vote_value - access.vote
            access.vote = vote_value
            cheatsheet.votes += differenz
            
        else:
            flash("Ungültiger Vote!", "error")
            return redirect(url_for("index"))


        db.session.commit()
        flash("Vote registered!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error updating vote: {str(e)}", "danger")
    
    return redirect(url_for("index"))



# DB
#@app.route("/create-tables")
#def create_tables():
#    with app.app_context():
#        db.create_all()
#    return "Database tables created!"

@app.route("/insert/sample")
def insert_sample():
    try:
        if User.query.first():
            return "Daten existieren bereits!"
        user1 = User(email="cooperwoolley@gmail.com", username="Cooper", pw=generate_password_hash("Cooper"), credits=100, userart="admin")
        user2 = User(email="jacobgotter@gmail.com", username="Jacob", pw=generate_password_hash("Jacob"), credits=101, userart="admin")

        db.session.add_all([user1, user2])
        db.session.commit()

        return "Daten erfolgreich implementiert!"
    except Exception as e:
        db.session.rollback()
        return f"Error inserting sample data: {str(e)}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)