from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)

# Initialize Limiter (limit requests based on IP address)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["25 per day"]  # 25 requests per user per day
)

# Initialize Token-based authentication
auth = HTTPTokenAuth(scheme="Bearer")

# Example tokens (in real-world, store these securely in a database)
tokens = {
    "user1_token": "User1",
    "user2_token": "User2"
}

# Token verification function
@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
    return None

# Define the 'Hello World' route with rate limiting and authentication
@app.route('/hello', methods=['GET'])
@auth.login_required  # Require authentication
@limiter.limit("25 per day")  # Limit to 25 requests per user per day
def hello():
    # Get the echo message from the query parameter
    echo_message = request.args.get('echo', 'World')
    return f"Hello, {echo_message}!"

# Handle rate limit exceeded errors
@app.errorhandler(429)
def ratelimit_handler(e):
    return f"Rate limit exceeded: {e.description}", 429

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)


#This is what the Request will look like 

# URL =>  GET /hello?echo=PostmanTest HTTP/1.1
# Headers => [Authorization: Bearer user1_token]

