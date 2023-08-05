from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///sqlite.db', echo=True, pool_recycle=7200)
metadata = MetaData()

users = Table('Users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(40), unique=True),
              Column('passwd', String(64)),
              Column('realname', String(40))
              )

users_history = Table('Users_history', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user', ForeignKey('Users.id')),
                      Column('login_time', DateTime),
                      Column('address', String(200))
                      )

contacts_users = Table('Contacts_users', metadata,
                       Column('user', ForeignKey('Users.id')),
                       Column('contacts', ForeignKey('Users.id')),
                       )

contacts = Table('Contacts', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('user', ForeignKey('Users.id')),
                 Column('contacts', ForeignKey('Users.id')),
                 )


class User:
    """
    Class for user table
    """
    def __init__(self, name, passwd, realname=None):
        self.id = None
        self.name = name
        self.passwd = passwd
        self.realname = realname

    # def __repr__(self):
    #     return "<User ('%s','%s')>" % (self.name, self.realname)


class UsersHistory:
    """
    Class for History table
    """
    def __init__(self, user, login_time, address):
        self.id = None
        self.user = user
        self.login_time = login_time
        self.address = address


class Contacts:
    """
    Class for contacts table
    """
    def __init__(self, user, contact):
        self.user = user
        self.contacts = contact


metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

mapper(User, users)
mapper(UsersHistory, users_history)
mapper(Contacts, contacts)


def add_users(name, address, passwd=None, realname=None):
    """
    function for add user in user table and history table
    :param name: str
    :param address: str
    :param passwd: str
    :param realname:
    :return: None
    """
    user_table = session.query(User).filter_by(name=name)
    if not user_table.count():
        user_new = User(name, passwd)
        session.add(user_new)
        session.commit()
    else:
        user_new = user_table.first()

    history = UsersHistory(user_new.id, datetime.now(), address)
    session.add(history)

    session.commit()


def add_contact(from_name, to_name):
    """
    Function for add contact in table
    :param from_name: str
    :param to_name: str
    :return: None
    """
    from_user = session.query(User).filter_by(name=from_name).first()
    contact = session.query(User).filter_by(name=to_name).first()
    if not from_user or not contact or session.query(Contacts).filter_by(user=from_name, contacts=to_name).count():
        return
    new_contact = Contacts(from_user.id, contact.id)
    session.add(new_contact)
    session.commit()


def get_contact(from_name):
    """
    Function for get contact from contacts table
    :param from_name: str
    :return: None
    """
    user = session.query(User).filter_by(name=from_name).one()
    list_contact = session.query(Contacts, User).filter_by(user=user.id).join(User, Contacts.contacts == User.id)

    return [cont[1].name for cont in list_contact.all()]


def del_contact(from_name, to_name):
    """
    Function for deleting contacts from contacts table
    :param from_name: str
    :param to_name: str
    :return: None
    """
    from_user = session.query(User).filter_by(name=from_name).first()
    contact = session.query(User).filter_by(name=to_name).first()
    if not from_user or not contact:
        return
    session.query(Contacts).filter(Contacts.user == from_user.id, Contacts.contacts == contact.id).delete()
    print(f'DELETE!!!')
    session.commit()


def get_users():
    """
    Function for get user from Users table
    :return: list
    """
    list_users = session.query(User)

    return [user.name for user in list_users]


def get_hash(name):
    """
    Function for get hash from Users table
    :param name: str
    :return: str
    """
    user = session.query(User).filter_by(name=name).first()
    return user.passwd


if __name__ == '__main__':
    print(get_users())
    print(get_hash('alex'))
