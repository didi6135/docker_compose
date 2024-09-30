from flask import Blueprint, jsonify, request
from config.postgres_config import get_postgres_connection
from config.redis_config import r

connection_blueprint = Blueprint('connection', __name__)


# route to check connection
@connection_blueprint.route('/')
def index():
    return "Welcome to the Flask-PostgreSQL App!"



# Route to register a new user (store email in PostgreSQL, password in Redis)
@connection_blueprint.route('/register', methods=['POST'])
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
@connection_blueprint.route('/login', methods=['POST'])
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