from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///client_sqlite.db', echo=True, pool_recycle=7200)
metadata = MetaData()

users = Table('Users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(40), unique=True),
              Column('realname', String(40))
              )

users_history = Table('Users_history', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user', ForeignKey('Users.id')),
                      Column('direction', String),
                      Column('message', Text),
                      Column('time', DateTime)
                      )


class User:
    """
    Class for User table
    """
    def __init__(self, name, realname=None):
        self.id = None
        self.name = name
        self.realname = realname


class UsersHistory:
    """
    Class for history table
    """
    def __init__(self, user, direction, message, time):
        self.id = None
        self.user = user
        self.direction = direction
        self.message = message
        self.time = time


metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

mapper(User, users)
mapper(UsersHistory, users_history)


def add_users(name, direction, message, realname=None):
    """
    Function for add users in User table
    :param name: str
    :param direction: str
    :param message: str
    :param realname:
    :return: None
    """
    user_table = session.query(User).filter_by(name=name)
    if not user_table.count():
        user_new = User(name)
        session.add(user_new)
        session.commit()
    else:
        user_new = user_table.first()

    history = UsersHistory(user_new.id, direction, message, time=datetime.now())
    session.add(history)
    session.commit()


def get_contact():
    """
    Function for get contacts from User table
    :return: None
    """
    list_contact = session.query(User)

    return [user.name for user in list_contact]


def get_history(user):
    """
    Function for get history from History table
    :param user: str
    :return: None
    """
    print('========------GET HISTORY-------=============')
    user_table = session.query(User).filter_by(name=user).first()
    query = session.query(UsersHistory).filter_by(user=user_table.id)

    return [(history_row.user, history_row.direction, history_row.message, history_row.time)
            for history_row in query.all()]


# a = get_contact()
# print(a)
