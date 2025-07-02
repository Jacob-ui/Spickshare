import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash #https://youtu.be/dam0GPOAvVI?t=5750
from flask_login import LoginManager, login_user, login_required, logout_user, current_user #https://youtu.be/dam0GPOAvVI?t=6589
from models import User, db
from models import Cheatsheet

app = Flask(__name__, instance_relative_config=True) #https://claude.ai/share/644c973d-59db-4614-8e57-cf71e15b4903 to fix multiple instance folder bug


# Konfiguration
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "spickshare.db")}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False 
)

app.instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance') #https://claude.ai/share/644c973d-59db-4614-8e57-cf71e15b4903 to fix multiple instance folder bug
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "spickshare.db")}'

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
print("Database path:", app.config['SQLALCHEMY_DATABASE_URI'])

# Startseite
@app.route('/')
def start():
    return redirect(url_for('index'))

@app.route('/index/')
def index():
    cheatsheets = Cheatsheet.query.all()
    
    # Optional: Cheatsheets als Liste von Dictionaries vorbereiten für das Template
    eintraege = []
    for sheet in cheatsheets:
        eintraege.append({
            'id': sheet.id,
            'titel': sheet.title,
            'beschreibung': sheet.description,
            'prof': '',  # Falls du Professor-Name aus sheet.professor_id laden willst, musst du noch joinen
            'score': str(sheet.votes),
        })
    
    return render_template('index.html', eintraege=eintraege, user=current_user) #https://youtu.be/dam0GPOAvVI?t=7011

#Login:
@app.route('/login/', methods=['GET', 'POST']) #https://youtu.be/dam0GPOAvVI?t=3449 für die GET und POST Teile des Codes
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('password')

        if not username or not pw:
            error_msg = 'Please fill out both fields!'
        else:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.pw, pw):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Username or password incorrect!', 'error')

    return render_template('login.html')


# Registrierung:
@app.route('/register/', methods=['GET', 'POST']) #
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        pw = request.form.get('password')
        pw2 = request.form.get('password2')


        if not email or not username or not pw or not pw2:
            flash('Bitte fülle alle Felder aus.', 'error')
        elif pw != pw2:
            flash('Passwörter stimmen nicht überein!', 'error')
        else:
            try: 
                user_exists = User.query.filter(
                    (User.username == username) | (User.email == email)
                ).first()
                if user_exists:
                    flash('Benutzername oder E-Mail existiert bereits.','error')
                else:
                    new_user = User(
                        username=username,
                        pw=generate_password_hash(pw),
                        email=email,
                        credits=0,
                        userart='not verified'
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    
                    flash('Registrierung erfolgreich! Bitte einloggen.', 'success')
                    return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Database error: {str(e)}', 'error')

    return render_template('register.html')

@app.route("/logout")
@login_required #https://youtu.be/dam0GPOAvVI?t=6715
def logout():
    logout_user()
    return redirect(url_for('index'))

    
#upload cheatsheets with html input https://www.youtube.com/watch?v=GQLRVhXnZkE&t=127s bis 4:40 und https://www.youtube.com/watch?v=pPSZpCVRbvQ gesamt
@app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        # Nur das Uploadformular anzeigen
        return render_template('upload.html')

    # POST: Daten verarbeiten
    file = request.files.get('file')
    title = request.form.get('title')
    description = request.form.get('description')

    if not file or file.filename == '':
        flash("Keine Datei ausgewählt!", "error")
        return redirect(url_for('upload'))

    if not title:
        flash("Titel darf nicht leer sein.", "error")
        return redirect(url_for('upload'))
    
    if not description:
        flash("Beschreibung darf nicht leer sein.", "error")
        return redirect(url_for('upload'))
    
    if not file.filename.lower().endswith('.pdf'):
        flash("Nur PDF-Dateien sind erlaubt.", "error")
        return redirect(url_for('upload'))

    try:
        new_sheet = Cheatsheet(
            title=title,
            description=description,
            pdf_datei=file.read(),
            user_id=current_user.id
        )
        db.session.add(new_sheet)
        db.session.commit()

        flash(f"Upload erfolgreich: {file.filename}", "success")
        return redirect(url_for('index'))

    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Hochladen: {str(e)}", "error")
        return redirect(url_for('upload'))

# Voting +/-
@app.route("/vote", methods=["POST"])
@login_required
def vote():
    eintrag_id = request.form.get('id') # fragt id vom sheet an
    vote_input = request.form.get('Voteinput') # liest aus index den +/- Button aus
    for eintrag in eintrag:
        if eintrag['id'] == eintrag_id:
            score = int(eintrag['score'])
            if vote_input == '+':
                score +=1
            elif vote_input == '-':
                score -=1
            eintrag['score'] = str(score) # speichert score
            break
    return render_template('index.html', eintraege=eintrag)



# DB
@app.route('/create-tables')
def create_tables():
    with app.app_context():
        db.create_all()
    return 'Database tables created!'

@app.route('/insert/sample')
def insert_sample():
    try:
        if User.query.first():
            return 'Daten existieren bereits!'
        user1 = User(email="cooperwoolley@gmail.com", username="Cooper", pw=generate_password_hash("Cooper"), credits=100, userart="admin")
        user2 = User(email="jacobgotter@gmail.com", username="Jacob", pw=generate_password_hash("Jacob"), credits=101, userart="admin")

        db.session.add_all([user1, user2])
        db.session.commit()

        return 'Daten erfolgreich implementiert!'
    except Exception as e:
        db.session.rollback()
        return f'Error inserting sample data: {str(e)}'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)