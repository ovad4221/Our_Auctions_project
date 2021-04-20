from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField,\
    TextAreaField, SubmitField, BooleanField, SelectField, FloatField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired
import sqlalchemy
import datetime


class RegisterUser(FlaskForm):
    name = StringField('Имя пользователя:', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя:', validators=[DataRequired()])
    patronymic = StringField('Отчество пользователя:', validators=[DataRequired()])
    age = IntegerField('Возраст:', validators=[DataRequired()])
    email = EmailField('Почта:', validators=[DataRequired()])
    position = StringField('Где работаете?', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
    # надо добавить загрузку фото


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    # по факту эта галочка не на что не влияет
    remember_me = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Войти')


class AddThing(FlaskForm):
    ed_izm_size = ['м', 'см', 'дюйм', 'фут']
    ed_izm_mass = ['кг', 'г', 'т', 'фунт']
    ed_izm_money = ['$', '€', '₽']

    name = StringField('Название: ', validators=[DataRequired()])
    height = FloatField("Высота: ")
    width = FloatField("Ширина: ")
    long = FloatField("Длина: ")
    units_size = SelectField('Единицы измерения размеров: ', choices=ed_izm_size)
    weight = FloatField("Масса: ")
    units_mass = SelectField('Единицы измерения массы: ', choices=ed_izm_mass)
    about = TextAreaField("Описание: ")
    colour = StringField('Цвет: ')
    price = FloatField('Цена: ', validators=[DataRequired()])
    units_money = SelectField('Валюта: ', choices=ed_izm_money)
    count = IntegerField('Кол-во: ', validators=[DataRequired()])
    # photos = MultipleFileField('Загрузите фото товара: ')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    submit = SubmitField('Принять')


class LotForm(FlaskForm):
    ed_izm_money = ['$', '€', '₽']

    name = StringField('Название: ', validators=[DataRequired()])
    about = TextAreaField("Описание: ")
    price = FloatField('Стартовая цена: ')
    units_money = SelectField('Валюта: ', choices=ed_izm_money)

    submit = SubmitField('Принять')


class AddThingToLot(FlaskForm):
    count = StringField('Количество: ', validators=[DataRequired()])

    submit = SubmitField('Принять')

