from flask import Flask
from oauth2client import client

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/oauth2callback')
def oauth2callback():
    pass


if __name__ == '__main__':
    app.secret_key = '3512a68c-3b77-474f-b807-0a24d73ac98b'

