#!/bin/python 
from flask import Flask, request, jsonify, g
import sqlite3
import poetID

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
    return jsonify(poetID.peotid())

@app.route('/poet')
def poet():
    if request.args.get('id'):
        try:
            poetid = request.args.get('id')
            print(poetid)
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
        return 'TEST'
    
    return homepage()

if __name__ == "__main__":
    app.run(debug=True)


