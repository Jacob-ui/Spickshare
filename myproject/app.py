import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash #https://youtu.be/dam0GPOAvVI?t=5750
from flask_login import LoginManager, login_user, login_required, logout_user, current_user #https://youtu.be/dam0GPOAvVI?t=6589
from models import User, db, Cheatsheet, UserCheatsheetAccess
from io import BytesIO #https://youtu.be/pPSZpCVRbvQ?t=322
import PyPDF2 as pdf #https://youtu.be/OdIHUdQ1-eQ?t=99
from sqlalchemy import func
import stripe #https://docs.stripe.com/api?lang=python
from functools import wraps #https://www.freecodecamp.org/news/python-decorators-explained-with-examples/

stripe.api_key = "sk_test_51RjIRVD6YuO3EM7xUfa6VRRR8JRJjE2uhuzUN7zTLUn9QqYRebXWoNA7CQHHovmszLXkzNzPFpyZ4Uk0hntf7oum00JesViHM7"  # Dein Secret Key von Stripe
YOUR_DOMAIN = "http://localhost:5000"  #https://docs.stripe.com/checkout/fulfillment
app = Flask(__name__, instance_relative_config=True) #https://claude.ai/share/644c973d-59db-4614-8e57-cf71e15b4903 to fix multiple instance folder bug

print("Tabelle 'order' wurde gelöscht.")

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



    if not file or file.filename == "":#Fehler abfangen und mit flash ausgeben https://flask.palletsprojects.com/en/latest/patterns/fileuploads/#handling-uploads
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
    if request.method == "POST":
        quantity = request.form.get("quantity")

        if not quantity or not quantity.isdigit() or int(quantity) <= 0:
            flash("Bitte gib eine gültige Anzahl an Credits ein.", "error")
            return redirect(url_for("buy_credits"))

        quantity = int(quantity)
        try:
            session = stripe.checkout.Session.create( #https://docs.stripe.com/api/checkout/sessions/create
                payment_method_types=['card'],#https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-payment_method_types
                line_items=[{
                    'price_data': {#https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-line_items-price_data
                        'currency': 'eur',
                        'unit_amount': quantity * 100,  # 1 Credit = 1 EUR
                        'product_data': {#https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-line_items-price_data-product_data
                            'name': f'{quantity} Credits',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',#https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-mode
                success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',#https://stripe.com/docs/payments/checkout/fulfill-orders
                cancel_url=url_for('buy_credits', _external=True),#https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-cancel_url
                metadata={#https://stripe.com/docs/api/checkout/sessions/create#create-checkout-session-metadata
                    "user_id": current_user.id,
                    "credits": quantity
                }
            )
            return redirect(session.url, code=303)

        except Exception as e:
            flash(f"Fehler beim Erstellen der Stripe-Session: {str(e)}", "error")
            return redirect(url_for("buy_credits"))

    return render_template("buy-credits.html")

@app.route("/payment-success")
@login_required
def payment_success():
    session_id = request.args.get("session_id")
    if not session_id:
        flash("Keine Session-ID gefunden.", "error")
        return redirect(url_for("index"))

    try:
        session = stripe.checkout.Session.retrieve(session_id) #https://stripe.com/docs/api/checkout/sessions/retrieve

        # Sicherheit: Nutzer darf nur seine eigene Zahlung bestätigen
        if str(current_user.id) != session.metadata["user_id"]:
            flash("Unberechtigter Zugriff auf Zahlung.", "error")
            return redirect(url_for("index"))

        credits = int(session.metadata["credits"])
        current_user.credits += credits
        db.session.commit()

        flash(f"Zahlung erfolgreich! {credits} Credits wurden deinem Konto gutgeschrieben.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Verarbeiten der Zahlung: {str(e)}", "error")

    return redirect(url_for("account"))


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

@login_required
def has_access(cheatsheet_id):
    access = UserCheatsheetAccess.query.filter_by(
        user_id = current_user.id,
        cheatsheet_id = cheatsheet_id
    ).first()
    if access:
        return True
    else:
        return False

def check_user_access(cheatsheet_id): #https://claude.ai/share/882bbdab-e385-445d-a3f9-b3d34192b12e has_access konnte in index.html nicht ohne seperate Template Functions ausgeführt werden
    if not current_user.is_authenticated:
        return False
    
    access = UserCheatsheetAccess.query.filter_by(
        user_id=current_user.id,
        cheatsheet_id=cheatsheet_id
    ).first()
    return access is not None

@app.context_processor #https://claude.ai/share/882bbdab-e385-445d-a3f9-b3d34192b12e has_access konnte in index.html nicht ohne seperate Template Functions ausgeführt werden
def inject_functions():
    return dict(has_access=check_user_access)

@app.route("/account")
@login_required
def account(): #https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_working_with_joins.htm für inner join Befehl
    cheatsheet_access = db.session.query(UserCheatsheetAccess,Cheatsheet).join(
        Cheatsheet,UserCheatsheetAccess.cheatsheet_id == Cheatsheet.id).filter(
        UserCheatsheetAccess.user_id == current_user.id).all()

    # Cheatsheets, die der User selber hochgeladen hat
    uploaded_cheatsheets = Cheatsheet.query.filter_by(user_id=current_user.id).all() #https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#simple-equality-filters

    #Anzahl der likes der eigenen Cheatsheets
    total_likes = db.session.query(func.sum(Cheatsheet.votes)).filter(#https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.func.sum
        Cheatsheet.user_id == current_user.id,
        Cheatsheet.votes > 0
    ).scalar() or 0

    return render_template("account.html", user = current_user, cheatsheet_access = cheatsheet_access, uploaded_cheatsheets=uploaded_cheatsheets, total_likes=total_likes)

def admin_required(func): #https://www.freecodecamp.org/news/python-decorators-explained-with-examples/

    @wraps(func)
    def check(*args, **kwargs):
        if not current_user.is_authenticated or current_user.userart != "admin":
            return redirect(url_for("index"))
        return func(*args, **kwargs)
    return check


@app.route("/all-cheatsheets/")
@admin_required
def all_cheatsheets(): #https://youtu.be/80b8n3ib7jo?t=336
    cheatsheets = Cheatsheet.query.all()

    cheatsheets_data = []
    for cheatsheet in cheatsheets:
        cheatsheet_dict = {
         'id': cheatsheet.id,
            'title': cheatsheet.title,
            'description': cheatsheet.description,
            'creditcost': cheatsheet.creditcost,
            'module': cheatsheet.module,
            'professor': cheatsheet.professor,
            'user_id': cheatsheet.user_id,
            'votes': cheatsheet.votes,
            'created_at': cheatsheet.created_at.isoformat() if cheatsheet.created_at else None, 
            'has_pdf': cheatsheet.pdf_datei is not None 
        }
        cheatsheets_data.append(cheatsheet_dict)

    return jsonify({
        'status': 'success',
        'count': len(cheatsheets_data),
        'cheatsheets': cheatsheets_data
    })


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