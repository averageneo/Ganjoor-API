from flask import g, jsonify
from poets_glossary import poets_name_glossary

def query(verse):
    # Checking verse order in DB
    verse_order = int(verse[2])

    """
    each verse is in one field in DB, I have to check it's order so I can get next and previous
    related verses the random verse chosen by user.
    """
    order_count = 1 # Helps me to see how many times While_loop has been run.
    while True:
        new_id = (verse[0] + order_count) # Get the next verse of the random verse
        order = g.cur.execute('SELECT * FROM verses WHERE id = ?', (new_id,))
        order_query = order.fetchone()
        if order_query[2] == 1: # checks if the next verse is related to random one
            break 
        else:
            order_count += 1

    # Total verses of the random poem        
    order_sum = verse_order+order_count 

    poem = []
    for i in range(verse[0], (verse[0] + order_sum)):
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
