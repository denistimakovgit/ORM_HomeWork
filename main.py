import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

login = "postgres"
password = "postgres"
data_base = "postgres"
host = "localhost"
port = "5432"
DSN = f"postgresql://{login}:{password}@{host}:{port}/{data_base}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

#создание записей в БД
def insert_data():
    """
    функция считывает данные из json файла
    и записывает их в БД
    """
    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for key, value in data.items():
        if key == "publisher":
            for i in range(0, len(value)):
                publisher_row = Publisher(
                    publisher_id=value[i]['publisher_id'],
                    name=value[i]['name']
                )
                session.add(publisher_row)
        elif key == "book":
            for i in range(0, len(value)):
                book_row = Book(
                    book_id=value[i]['book_id'],
                    title=value[i]['title'],
                    publisher_id=value[i]["publisher_id"]
                )
                session.add(book_row)
        elif key == "shop":
            for i in range(0, len(value)):
                shop_row = Shop(
                    shop_id=value[i]['shop_id'],
                    shop_name=value[i]['shop_name']
                )
                session.add(shop_row)
        elif key == "stock":
            for i in range(0, len(value)):
                stock_row = Stock(
                    stock_id=value[i]['stock_id'],
                    book_id=value[i]['book_id'],
                    shop_id=value[i]['shop_id'],
                    count=value[i]['count']
                )
                session.add(stock_row)
        elif key == "sale":
            for i in range(0, len(value)):
                sale_row = Sale(
                    sale_id=value[i]['stock_id'],
                    price=value[i]['price'],
                    sale_date=value[i]['sale_date'],
                    stock_id=value[i]['stock_id'],
                    count=value[i]['count']
                )
                session.add(sale_row)
    session.commit()

def search_data():
    """
    функция выполняет поиск данных по имени автора книги или по его идентификатору
    """
    insert_data()
    choise_of_search = int(input("Для поиска по ID введите 1, для поиска по имени введите 2:"))
    if choise_of_search == 1:
        pub_name = int(input("Введите идентификатор издателя: "))
        for c in session.query(
                Book.title,
                Shop.shop_name,
                Sale.price,
                Sale.count,
                Sale.sale_date
        ).join(Stock.shop).join(Stock.book).join(Sale, Stock.stock_id == Sale.stock_id).join(Book.publisher).filter(
            Publisher.publisher_id == pub_name).all():
            print(f'{c.title:^10} | {c.shop_name:^10} | {c.price * c.count:^10} | {c.sale_date}')
    elif choise_of_search == 2:
        pub_name = input("Введите имя издателя: ")
        for c in session.query(
                Book.title,
                Shop.shop_name,
                Sale.price,
                Sale.count,
                Sale.sale_date
            ).join(Stock.shop).join(Stock.book).join(Sale, Stock.stock_id == Sale.stock_id).join(Book.publisher).filter(Publisher.name.like(f"%{pub_name}%")).all():
            print(f'{c.title:^10} | {c.shop_name:^10} | {c.price*c.count:^10} | {c.sale_date}')

    session.close()

if __name__ == '__main__':
    search_data()