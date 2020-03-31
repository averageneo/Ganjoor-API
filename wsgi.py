from flask import Flask, request, jsonify, g, render_template
import sqlite3
from random_verse_generator import random_verse_generator
from poets_glossary import poets_name_glossary
from verses_query import query
 

app = Flask(__name__)
app.url_map.strict_slashes = False
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


# Decorator to show poets and their id's in JSON text format
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
@app.route('/poet/<name_id>')
def poet(name_id=None):
    if name_id is not None:
        if any(x.isalpha() for x in name_id) == False:
            poetid = name_id
            poet_info = g.cur.execute('SELECT * FROM poets WHERE id = ?', (poetid,))
        else:
            poet_english_name = name_id
            poet_persian_name = poets_name_glossary.get(name_id)
            poet_info = g.cur.execute('SELECT * FROM poets WHERE name = ?', (poet_persian_name,))
        
        poet = poet_info.fetchone()
        return jsonify(poet[3])


# Decorator to generate verses
@app.route('/random/')
@app.route('/random/<poet>/')
def verses(poet=None):
    if poet is None:
        random_verse = random_verse_generator()
        # Selecting the random row ID in DB.
        verse_id = g.cur.execute('SELECT * FROM verses WHERE id = ?', (random_verse,))
        verse = verse_id.fetchone()
    else:
        random_poem_id = random_verse_generator(poet)
        if random_poem_id == 'Error':
            return 'No poet with this name'
        else:    
            verse_id = g.cur.execute('SELECT * FROM verses WHERE poemId = ?', (random_poem_id,))
            verse = verse_id.fetchone()
    
    return jsonify(query(verse))


@app.route('/glossary')
def glossary():
    return jsonify(poets_name_glossary)


if __name__ == "__main__":
    app.run()
