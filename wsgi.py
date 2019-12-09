#!/bin/python 
from flask import Flask, request, jsonify, g, render_template
import sqlite3
from random import randint
from poets_glossary import poets_name_glossary

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
    return render_template('index.html')

# Decorator to show poets and their id's in JSON format
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

# Decorator to show poets Biographies.
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




def random_verse_generator():
    # Generates a random number for the rows in DB
    random_verse = randint(1, 1384003)
    
    # Selecting the random row ID in DB.
    verse_id = g.cur.execute('SELECT * FROM verses WHERE id = ?', (random_verse,))
    verse = verse_id.fetchone()
    
    # Checking verse order in DB
    verse_order = int(verse[3])

    """
    each verse is in one field in DB, I have to check it's order so I can get next and previous
    related verses the random verse chosen by user.

    """
    order_count = 1 # Helps me to see how many times While_loop has been run.
    while True:
        new_id = (random_verse + order_count) # Get the next verse of the random verse
        order = g.cur.execute('SELECT * FROM verses WHERE id = ?', (new_id,))
        order_query = order.fetchone()
        if order_query[3] == 0: # checks if the next verse is related to random one
            break 
        else:
            order_count += 1

    # Total verses of the random poem        
    order_sum = verse_order+order_count    
    return order_sum, random_verse, verse
    


# Decorator to generate verses
@app.route('/verses')
def verses():
    # Random verse request
    verse_req = request.args.get('verse') 
    # less than helps user the get poems with limited verses count
    lessthan = request.args.get('lessthan')
    if verse_req == 'random':
        if lessthan is not None:
            if int(lessthan) < 3:
                return '"Lessthan" argument can not be less than 3!'

            while True:
                order_sum, random_verse, verse = random_verse_generator()
                if int(order_sum) < int(lessthan):
                    break
        else:
            order_sum, random_verse, verse = random_verse_generator()

        poem = []
        for i in range(random_verse, (random_verse + order_sum)):
            Select_whole_poem = g.cur.execute('SELECT * FROM verses WHERE id = ?', (i,))
            fetch_poem = Select_whole_poem.fetchone()
            verses = str(fetch_poem[4])
            poem.append(verses)

        ## Query for the Poet name and Poem category
        Poem_ID = verse[1]
        select_poems = g.cur.execute('SELECT * FROM poems WHERE id = ?', (Poem_ID,))
        query_poems = select_poems.fetchone()


        # Poem category
        category_id = int(query_poems[1])
        select_category  = g.cur.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
        fetch_category = select_category.fetchone()
        poem_category = fetch_category[2]
        if poem_category not in poets_name_glossary.values() :    
            poem.insert(0, str(poem_category))

        # poet name
        url = str(query_poems[3])
        if bool(url) == True:
            poet_name = url.split('/')[3]
            poet_name = poets_name_glossary[poet_name]
            poem.insert(0, poet_name)

        return jsonify(poem)

    else:
        return 'Are you sure of the Request?!'

    


if __name__ == "__main__":
    app.run(debug=True)
