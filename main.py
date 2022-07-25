import os
from pprint import pprint

import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
from models import create_tables, Publisher, Book, Shop, Stock, Sale


class GetParam:
    def __init__(self):
        self.DB_CONN = os.getenv('TC_VCS_WEB_DB_CONN').split(';')
        self.driver = self.DB_CONN[0].split(':')[0]
        self.host = self.DB_CONN[0].split(':')[1].split('=')[1]
        self.port = self.DB_CONN[1].split('=')[1]
        self.login = open('log_pass.txt').readlines()[1].strip('\n')
        self.password = open('log_pass.txt').readlines()[3].strip('\n')
        self.db_name = open('log_pass.txt').readlines()[5].strip('\n')
        self.DSN = f'{self.driver}://{self.login}:{self.password}@{self.host}:{self.port}/{self.db_name}'


if __name__ == '__main__':
    dataconn = GetParam()

    DSN = f'{dataconn.driver}://{dataconn.login}:{dataconn.password}@{dataconn.host}:{dataconn.port}/{dataconn.db_name}'

    engine = sqlalchemy.create_engine(dataconn.DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('fixtures.json') as file_:
        data = json.load(file_)

    entity = {'publisher': Publisher,
              'book': Book,
              'shop': Shop,
              'stock': Stock,
              'sale': Sale}

    for string_ in data:
        session.add(entity[string_['model']](id=string_['pk'], **string_['fields']))
        session.commit()

    query_ = session.query(Shop).join(Stock, Stock.id_shop == Shop.id).join(Book, Stock.id_book == Book.id).join(
        Publisher, Publisher.id == Book.id_publisher)

    publisher_ = input()

    if publisher_.isdigit():
        publisher_ = int(publisher_)
        print(f'Магазины где есть книги автора c id {publisher_}:')
        for shops in query_.filter(Publisher.id == publisher_).all():
            print(shops)
    else:
        print(f'Магазины где есть книги автора {publisher_}:')
        for shops in query_.filter(Publisher.name == publisher_).all():
            print(shops)

    session.close()
