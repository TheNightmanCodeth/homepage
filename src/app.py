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

