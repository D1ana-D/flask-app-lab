import logging
from flask import render_template, request, redirect, url_for, flash
from . import app
from app.forms import ContactForm

logging.basicConfig(
    filename='contact_log.txt',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title="Резюме - Дацьо Діана")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        logging.info(f"Contact Form Submission: Name={name}, Email={email}, Phone={phone}, Subject={subject}, Message={message}")
        
        flash("Ваше повідомлення успішно надіслано та збережено!", "success")
        return redirect(url_for('contacts'))
        
    return render_template('contacts.html', title="Контакти - Дацьо Діана", form=form)

@app.route('/homepage')
def home():
    agent = request.user_agent.string
    return render_template('resume.html', title="Головна", agent=agent)