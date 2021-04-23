from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, \
    TextAreaField, SubmitField, BooleanField, SelectField, FloatField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired
import sqlalchemy
import datetime

ed_izm_money = ['$ (USD)', '€ (EUR)', '₽ (RUB)', '¢ (AUD)', '₼ (AZN)', '£ (GBP)', '֏ (AMD)', 'Br (BYN)',
                'лв (BGN)', 'R$ (BRL)', 'ƒ (HUF)', '元 (HKD)', 'kr (DKK)', '₹ (INR)', '₸ (KZT)',
                'C$ (CAD)', 'с (KGS)', '¥ (CNY)', 'L (MDL)', 'kr (NOK)', 'zł (PLN)', 'lei (RON)', 'S$ (SGD)',
                'SM (TJS)', '₺ (TRY)', 'T (TMT)', "So'm (UZS)", '₴ (UAH)', 'Kč (CZK)', 'kr (SEK)',
                'Fr (CHF)', 'R (ZAR)', '₩ (KRW)', '円 (JPY)']


class RegisterUser(FlaskForm):
    name = StringField('Имя пользователя:', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя:', validators=[DataRequired()])
    patronymic = StringField('Отчество пользователя:')
    age = IntegerField('Возраст:', validators=[DataRequired()])
    email = EmailField('Почта:', validators=[DataRequired()])
    position = StringField('Где работаете?')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
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

    name = StringField('Название: ', validators=[DataRequired()])
    height = StringField("Высота: ")
    width = StringField("Ширина: ")
    long = StringField("Длина: ")
    units_size = SelectField('Единицы измерения размеров: ', choices=ed_izm_size)
    weight = StringField("Масса: ")
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
    name = StringField('Название: ', validators=[DataRequired()])
    about = TextAreaField("Описание: ")
    price = FloatField('Стартовая цена: ')
    units_money = SelectField('Валюта: ', choices=ed_izm_money)

    submit = SubmitField('Принять')


class AddThingToLot(FlaskForm):
    count = StringField('Количество: ', validators=[DataRequired()])

    submit = SubmitField('Принять')
