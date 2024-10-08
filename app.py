from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the GET request
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
