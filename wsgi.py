#!/bin/python 
from flask import Flask, request, jsonify, g
import sqlite3
from random import randint

app = Flask(__name__)

def makedb():
     return sqlite3.connect('database.sqlite')

@app.before_request
def befor_request():
    g.db = makedb()
    g.cur = g.db.cursor()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def homepage():
    return 'Welcome to Ganjoor-API'


@app.route('/poets')
def poets():
    g.cur.execute('SELECT * FROM poets')
    rows = g.cur.fetchall()
    poets = []
    for row in rows:
        poet={
        'Name': row[1],
        'ID': row[0]
        }
        poets.append(poet)

    return jsonify(poets)

@app.route('/poet')
def poet():
    if request.args.get('id'):
        try:
            poetid = request.args.get('id')
            poet_info = g.cur.execute('SELECT * FROM poets WHERE id = ?', (poetid,))
            poet = poet_info.fetchone()
            return jsonify(poet[3])
        except TypeError:
            return 'شاعری با این مشخصات وجود ندارد'
    else:
        return homepage()

@app.route('/verses')
def verses():
    if request.args.get('verse') == 'random':
        random_verse = randint(1, 1384003)
        verse_id = g.cur.execute('SELECT * FROM verses WHERE id = ?', (random_verse,))
        verse = verse_id.fetchone()
        verse_order = int(verse[3])

        order_count = 1
        while True:
            new_id = (random_verse + order_count)
            order = g.cur.execute('SELECT * FROM verses WHERE id = ?', (new_id,))
            order_query = order.fetchone()
            if order_query[3] == 1:
                break
            else:
                order_count += 1
        
        order_sum = verse_order+order_count
        final_verse = []
        for i in range(random_verse, (random_verse + order_sum)):
            fianl_query = g.cur.execute('SELECT * FROM verses WHERE id = ?', (i,))
            final_fetch = fianl_query.fetchone()
            verse = str(final_fetch[4])
            final_verse.append(verse)
            
        return jsonify(final_verse)

    return homepage()

if __name__ == "__main__":
    app.run(debug=True)


