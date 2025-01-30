from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, add_user, get_user, add_friend, get_friends, send_coins, get_chat_messages, add_chat_message

app = Flask(__name__)
app.secret_key = 'your_secret_key'
init_db()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_user(username, password)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username, password)
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    friends = get_friends(session['user_id'])
    return render_template('dashboard.html', friends=friends)

@app.route('/add_friend', methods=['POST'])
def add_friend():
    friend_id = request.form['friend_id']
    add_friend(session['user_id'], friend_id)
    return redirect(url_for('dashboard'))

@app.route('/send_coins', methods=['POST'])
def send_coins_route():
    recipient = request.form['recipient']
    amount = request.form['amount']
    send_coins(session['user_id'], recipient, amount)
    return redirect(url_for('dashboard'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        message = request.form['message']
        add_chat_message(session['user_id'], message)
    messages = get_chat_messages()
    return render_template('chat.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
