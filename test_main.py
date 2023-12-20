import sqlite3
import pytest
from main import create_tables, drop_tables


@pytest.fixture(scope='session')
def db_connection():
    connection = sqlite3.connect(':memory:')
    create_tables(connection)
    yield connection
    drop_tables(connection)
    connection.close()


@pytest.fixture(scope='function')
def create_table(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_table (
                       id INTEGER PRIMARY KEY,
                       name TEXT NOT NULL);''')
    db_connection.commit()
    yield
    cursor.execute('''DROP TABLE IF EXISTS test_table;''')
    db_connection.commit()


@pytest.fixture(scope='function')
def populate_nursery_with_dogs(db_connection):
    cursor = db_connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS dogs (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        breed TEXT NOT NULL,
        subbreed TEXT);''')
    db_connection.commit()

    cursor.execute("INSERT INTO dogs (name, breed) VALUES ('Dog1', 'Breed1');")
    cursor.execute("INSERT INTO dogs (name, breed) VALUES ('Dog2', 'Breed2');")
    cursor.execute("INSERT INTO dogs (name, breed) VALUES ('Dog3', 'Breed3');")
    db_connection.commit()

    yield
    cursor.execute("DELETE FROM dogs;")
    db_connection.commit()
