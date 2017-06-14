from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

#Index route should redirect to /projects
@app.route('/')
def index():
    return redirect(url_for("projects"))

#Projects page
@app.route('/projects')
def projects():
    return render_template('projects.html', context="projects")

#For hire page
@app.route('/for-hire')
def forhire():
    return render_template('coming_soon.html', context="for-hire")

#CloverOS - DEMO MODE
@app.route('/CloverOS')
def clover_os():
    return render_template('main.html', context="about")

#CloverOS - Downloads - DEMO MODE
@app.route('/CloverOS/get-clover')
def get_clover():
    return render_template('get-clover.html', context="download")

