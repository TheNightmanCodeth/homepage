import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
homepage = Flask(__name__, static_url_path='/static')
homepage.config.from_object(__name__)

homepage.config.update(dict(
    DATABASE=os.path.join(homepage.root_path, 'nightman.db'),
    SECRET_KEY='thegamelolol',
    USERNAME='dayman97',
    PASSWORD='password'
))
homepage.config.from_envvar('NIGHTMAN_SETTINGS', silent=True)
homepage.config['UPLOAD_FOLDER'] = 'uploads/'

def hook_db():
    """"Connects to sql database"""
    db = sqlite3.connect(homepage.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with homepage.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@homepage.cli.command('initdb')
def initdb_cmd():
    """runs init_db"""
    init_db()
    print ('Database initialized')

def get_db():
    """Opens db connection if one does not exist"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = hook_db()
    return g.sqlite_db

@homepage.teardown_appcontext
def close_db(error):
    """Closes db at the end of request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Routes
@homepage.route('/')
def home():
    db = get_db()
    query = db.execute('select title, description, repo, img, language from projects order by id desc')
    projects = query.fetchall()
    return render_template('main.html', projects=projects)

@homepage.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file!!')
            return jsonify({"error": "no file attached"})
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(homepage.config['UPLOAD_FOLDER'], filename))
            return jsonify({"Success": "File received!"})
    return render_template('ul.html')

@homepage.route('/get-file/<path:file>')
def get_file(file):
    return send_from_directory('uploads', file)

@homepage.route('/cirkit')
def cirkit():
    return render_template('cirkit.html')

@homepage.route('/maddie-is-dumb/<path:img>')
def maddiendtflw(img):
    return send_from_directory('static/img/mad', img)

@homepage.route('/img/<path:img>')
def retimg(img):
    return send_from_directory('static/img', img)

if __name__ == "__main__":
    homepage.run(host='0.0.0.0', debug=True)
