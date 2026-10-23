from flask import render_template, request
from . import app

@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title="Резюме - Дацьо Діана")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти - Дацьо Діана")

@app.route('/homepage')
def home():
    agent = request.user_agent.string
    return render_template('resume.html', title="Головна", agent=agent)