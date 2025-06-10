import os
from flask import Flask, redirect, url_for, render_template, request, jsonify
import db  # dein db.py Modul mit DB-Funktionen

app = Flask(__name__)

# Konfiguration
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'spickshare.sqlite')
)

# DB initialisieren
app.cli.add_command(db.init_db)  # CLI-Befehl aus db.py
app.teardown_appcontext(db.close_db_con)


@app.route('/')
def index():
    return redirect(url_for('lists'))


@app.route('/lists/')
def lists():
    db_con = db.get_db_con()
    lists_temp = db_con.execute('SELECT * FROM list ORDER BY name').fetchall()
    lists = []

    for list_temp in lists_temp:
        list_dict = dict(list_temp)
        sql = (
            'SELECT COUNT(complete) = SUM(complete) AS complete FROM todo '
            f'JOIN todo_list ON list_id={list_dict["id"]} AND todo_id=todo.id;'
        )
        complete = db_con.execute(sql).fetchone()['complete']
        list_dict['complete'] = complete
        lists.append(list_dict)

    if request.args.get('json') is not None:
        return jsonify(lists)
    else:
        return render_template('lists.html', lists=lists)



@app.route('/lists/<int:id>')
def list(id):
    db_con = db.get_db_con()
    list_name = db_con.execute('SELECT name FROM list WHERE id=?', (id,)).fetchone()

    if list_name is None:
        return "List not found", 404

    todos = db_con.execute(
        'SELECT id, complete, description FROM todo '
        'JOIN todo_list ON todo_id=todo.id AND list_id=? '
        'ORDER BY id;', (id,)
    ).fetchall()

    list_data = {
        'name': list_name['name'],
        'todos': [dict(todo) for todo in todos]
    }

    if request.args.get('json') is not None:
        return jsonify(list_data)
    else:
        return render_template('list.html', list=list_data)


@app.route('/insert/sample')
def run_insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'


if __name__ == '__main__':
    app.run(debug=True)