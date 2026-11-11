from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Обов'язкове поле"),
        Length(min=4, max=10, message="Довжина ім'я має бути від 4 до 10 символів")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Обов'язкове поле"),
        Email(message="Некоректний формат email")
    ])
    phone = StringField('Phone', validators=[
        DataRequired(message="Обов'язкове поле"),
        Regexp(r'^\+380\d{9}$', message="Формат телефону повинен бути: +380XXXXXXXXX")
    ])
    subject = SelectField('Subject', choices=[
        ('general', 'Загальне питання'),
        ('support', 'Технічна підтримка'),
        ('cooperation', 'Співпраця')
    ], validators=[DataRequired(message="Оберіть тему")])
    
    message = TextAreaField('Message', validators=[
        DataRequired(message="Обов'язкове поле"),
        Length(max=500, message="Максимальна довжина повідомлення — 500 символів")
    ])
    
    submit = SubmitField('Send Message')