import sqlite3

def connect_db():
    return sqlite3.connect('app.db')

def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS friends (user_id INTEGER, friend_id INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS coins (user_id INTEGER, amount INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat (user_id INTEGER, message TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_friend(user_id, friend_username):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username=?', (friend_username,))
    friend = c.fetchone()
    if friend:
        c.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (user_id, friend[0]))
        conn.commit()
    conn.close()

def get_friends(user_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE id IN (SELECT friend_id FROM friends WHERE user_id=?)', (user_id,))
    friends = c.fetchall()
    conn.close()
    return [friend[0] for friend in friends]

def send_coins(user_id, recipient_username, amount):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username=?', (recipient_username,))
    recipient = c.fetchone()
    if recipient:
        # Update sender's coins
        c.execute('UPDATE coins SET amount = amount - ? WHERE user_id = ?', (amount, user_id))
        # Update recipient's coins
        c.execute('INSERT INTO coins (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?',
                  (recipient[0], amount, amount))
        conn.commit()
    conn.close()

def get_chat_messages():
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT user_id, message FROM chat')
    messages = c.fetchall()
    conn.close()
    return [{'user_id': msg[0], 'message': msg[1]} for msg in messages]

def add_chat_message(user_id, message):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO chat (user_id, message) VALUES (?, ?)', (user_id, message))
    conn.commit()
    conn.close()
