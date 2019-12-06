# This will pull out all the poets with their ID's from the DB

import sqlite3
from pprint import pprint
def peotid():
    connect = sqlite3.connect('database.sqlite')
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM poets')
    rows = cursor.fetchall()

    poets = []
    for row in rows:
        poet={
        'Name': row[1],
        'ID': row[0]
        }
        poets.append(poet)

    return poets
