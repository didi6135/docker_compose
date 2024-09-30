from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import redis

from seed import create_table_if_not_exist, get_postgres_connection


app = Flask(__name__)

    
# Redis details
REDIS_HOST = 'redis-db'
REDIS_PORT = 6379


# Redis connection
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)



create_table_if_not_exist()

@app.route('/')
def index():
    return "Welcome to the Flask-PostgreSQL App!"


# Route to register a new user (store email in PostgreSQL, password in Redis)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    
    # Store email in PostgreSQL
    conn = get_postgres_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO users (email) VALUES (%s)", (email,))
    conn.commit()
    cur.close()
    conn.close()

    # Store password in Redis
    r.set(email, password)

    return jsonify({"message": "User registered successfully"})

# Route to log in (validate email from PostgreSQL and password from Redis)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    
    # Check if email exists in PostgreSQL
    conn = get_postgres_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid email"}), 400

    # Validate password from Redis
    stored_password = r.get(email)
    if stored_password != password:
        return jsonify({"error": "Invalid password"}), 400

    return jsonify({"message": "Login successful!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
