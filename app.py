from flask import Flask, render_template_string
import db

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    db.close_db()

@app.route('/')
def index():
    database = db.get_db()
    database.execute("INSERT INTO messages (text) VALUES (?)", ("Hallo Welt!",))
    database.commit()

    cur = database.execute('SELECT * FROM messages')
    messages = cur.fetchall()

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Hallo Welt mit DB</title></head>
        <body>
            <h1>Nachrichten aus der Datenbank:</h1>
            <ul>
                {% for msg in messages %}
                    <li>{{ msg['text'] }}</li>
                {% endfor %}
            </ul>
        </body>
        </html>
    ''', messages=messages)

if __name__ == "__main__":
    db.init_db(app)
    app.run(debug=True)
