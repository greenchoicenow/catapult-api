from flask import Flask, request, jsonify, make_response
import pyodbc
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection parameters
DATABASE_CONFIG = {
    'server': os.getenv('DB_SERVER'),
    'database': os.getenv('DB_DATABASE'),
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD')
}

# Secret key for JWT
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)


def token_required(f):
    """
    Decorator to require a token for routes.
    This function checks for the token in the query parameters and verifies it.
    If the token is missing or invalid, it returns an error.

    Args:
        f (function): The function to wrap.

    Returns:
        function: The wrapped function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # http://yourdomain.com/route?token=xxxxx
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


def get_database_connection():
    """
    Creates and returns a database connection.

    Returns:
        connection: A connection object to the SQL Server database.
    """
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=' + DATABASE_CONFIG['server'] + ';'
                              'DATABASE=' + DATABASE_CONFIG['database'] + ';'
                              'UID=' + DATABASE_CONFIG['username'] + ';'
                              'PWD=' + DATABASE_CONFIG['password'])
        return conn
    except Exception as e:
        print("Error connecting to database: ", e)
        return None

@app.route('/products', methods=['GET'])
@token_required
def get_products():
    """
    API endpoint to retrieve product information.
    Requires a valid token to access. Fetches product name and stock status
    from the database.

    Returns:
        json: A JSON response containing product information or an error
        message.
    """
    conn = get_database_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ProductName, StockStatus FROM Products")
        result = cursor.fetchall()
        return jsonify(result)
    else:
        return jsonify({'message': 'Database connection error'}), 500

@app.route('/login', methods=['GET'])
def login():
    """
    API endpoint for user login.
    Authenticates the user and provides a JWT token for accessing protected 
    endpoints.

    Returns:
        json: A JSON response containing the JWT token or an error message.
    """
    auth = request.authorization

    if auth and auth.username == 'admin' and auth.password == 'password':
        token = jwt.encode({
            'user': auth.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})

    return make_response(
        'Could not verify!',
        401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)
