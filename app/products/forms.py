from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[
        DataRequired(message="Обов'язкове поле"),
        Length(min=3, message="Назва повинна містити мінімум 3 символи")
    ])
    content = TextAreaField('Опис товару', validators=[
        DataRequired(message="Обов'язкове поле")
    ])
    price = DecimalField('Ціна ($)', places=2, validators=[
        DataRequired(message="Обов'язкове поле"),
        NumberRange(min=0.01, message="Ціна повинна бути більшою за 0")
    ])
    category = SelectField('Категорія', choices=[
        ('Electronics', 'Електроніка'),
        ('Computers', 'Комп\'ютери'),
        ('Smartphones', 'Смартфони'),
        ('Accessories', 'Аксесуари')
    ], validators=[DataRequired(message="Оберіть категорію")])
    
    quantity = IntegerField('Кількість', validators=[
        DataRequired(message="Обов'язкове поле"),
        NumberRange(min=0, message="Кількість не може бути від'ємною")
    ])
    image = FileField('Зображення товару', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Дозволено лише зображення PNG, JPG та JPEG!')
    ])
    submit = SubmitField('Зберегти товар')