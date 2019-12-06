#!/bin/python 
from flask import request, Flask
import sqlite3

connect = sqlite3.connect('database.sqlite')
cursor = connect.cursor()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    return hello


if __name__ == "__main__":
    app.run(debug=True)


