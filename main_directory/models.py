from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired


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
    team_leader = IntegerField('Лидер команды')
    job = TextAreaField("Содержание")
    work_size = IntegerField("На сколько работа в часах")
    collaborators = StringField("Поле для хранения id работников")
    category = IntegerField("Category")
    # можно запариться и сделать здесь разные слова
    submit = SubmitField('Дальше')


