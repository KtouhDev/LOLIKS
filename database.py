import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS friends (user_id INTEGER, friend_id INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS coins (user_id INTEGER, amount INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat (user_id INTEGER, message TEXT)''')
    conn.commit()
    conn.close()

# Add user, get user, add friend, get friends, send coins, get chat messages, add chat message functions here
