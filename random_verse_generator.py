from random import randint
from flask import g

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
