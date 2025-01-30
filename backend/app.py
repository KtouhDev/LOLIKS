from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import psycopg2  # Для работы с PostgreSQL
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Подключение к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="unichat_db",
        user="your_username",
        password="your_password"
    )
    return conn

# Login Route с корректной проверкой пользователя
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Проверяем наличие email и пароля
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    try:
        # Подключаемся к базе данных
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Выполняем запрос для поиска пользователя
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        # Проверяем пользователя
        if user and check_password_hash(user['password'], password):
            # Создаем JWT токен
            token = jwt.encode({
                'user_id': user['id'], 
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            # Закрываем соединение
            cur.close()
            conn.close()

            return jsonify({
                'token': token,
                'user_id': user['id'],
                'username': user['username']
            })
        else:
            # Закрываем соединение
            cur.close()
            conn.close()
            return jsonify({'message': 'Invalid credentials'}), 401

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return jsonify({'message': 'Database error'}), 500

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Проверяем наличие всех необходимых полей
    if not username or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Проверяем, существует ли уже пользователь с таким email
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        
        if existing_user:
            cur.close()
            conn.close()
            return jsonify({'message': 'User with this email already exists'}), 409

        # Хешируем пароль
        hashed_password = generate_password_hash(password, method='sha256')

        # Вставляем нового пользователя
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()

        # Закрываем соединение
        cur.close()
        conn.close()

        return jsonify({'message': 'User registered successfully'}), 201

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return jsonify({'message': 'Registration failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
