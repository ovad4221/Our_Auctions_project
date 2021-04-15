import datetime
import sqlalchemy
from .db_session import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)

    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # прайм можно будет купить на время(или как-то получить от разработчика)
    # или честно получить
    # как это сделать описано ниже
    is_prime = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)

    reviews = orm.relation('Review', back_populates='creator')

    # создавать свой аукцион может только проверенный пользователь
    # проверенным называется пользователь, совершивший не меньше 30 покупок
    # и выставивший не меньше 20 вещей (поле is_prime)
    # или админ(id = 1)
    auctions = orm.relation("Auction", back_populates='creator')

    # необходимо сделать еще загрузку файла, пока что пропустим
    photos = orm.relation("Photo", back_populates='user')

    things = orm.relation("Thing", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Thing(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'things'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    long = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    width = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    colour = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_price = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    bought = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    photos = orm.relation('Photo')
    # может не сработать нуллебел
    auction_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("auctions.id"), nullable=True)
    auction = orm.relation('Auction')


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    thing_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("things.id"), nullable=True)
    thing = orm.relation('Thing')
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"), nullable=True)
    user = orm.relation('User')


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    auctions = orm.relation("Auction", back_populates='category')


class Auction(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'auctions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # это полу исключительно для сообщения пользователю
    # о времени начала и конца аукциона
    when = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    entry_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)

    creator_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    creator = orm.relation('User')

    category_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("categories.id"))
    # категория аукциона: машины, старинное и тд
    category = orm.relation('Category')

    review_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("reviews.id"), nullable=True)
    review = orm.relation('Review')

    things = orm.relation("Thing", back_populates='auction')


class Review(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    auctions = orm.relation("Auction", back_populates='review')

    creator_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    creator = orm.relation("User")


class Ready(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'readies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # остальное будет в более поздних версиях
