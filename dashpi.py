import flask
import json
import hashlib
import os

import urllib.parse
import http.client
from oauth2client import client
from oauth2client import crypt

app = flask.Flask(__name__)
app.secret_key = '3512a68c-3b77-474f-b807-0a24d73ac98b'
app.debug = True

SCOPE = ['https://www.googleapis.com/auth/calendar.readonly',
			'https://www.googleapis.com/auth/gmail.readonly'
			]
#Use this URL if you're testing via multiple devices. xip.io is awesome
#REDIRECT_URL='http://www.192.168.0.196.xip.io:5000/oauth2callback'
REDIRECT_URL='http://localhost:5000/oauth2callback'


G_TOKEN_URL = 'https://www.googleapis.com/oauth2/v4/token'

@app.route('/')
def index():
	if 'google_credentials' in flask.session:
		return 'Hello World!'
	else:
		return flask.redirect(flask.url_for('login'), 302)

@app.route('/login')
def login():
	#return flask.render_template('login.html', auth_uri=auth_uri) 
	return flask.render_template('login.html')

@app.route('/oauth2callback', methods=['POST'])
def oauth2callback():
	token = flask.request.form['idtoken']
	# (Receive token by HTTPS POST)
	try:
		idinfo = client.verify_id_token(token, CLIENT_ID)
		# If multiple clients access the backend server:
		if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
			raise crypt.AppIdentityError("Unrecognized client.")
		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
			raise crypt.AppIdentityError("Wrong issuer.")
		if idinfo['hd'] != APPS_DOMAIN_NAME:
			raise crypt.AppIdentityError("Wrong hosted domain.")
	except crypt.AppIdentityError:
		# Invalid token
		return flask.redirect(flask.url_for('error/401'), 303)

	userid = idinfo['sub']

@app.route('/logout')
def logout():
	flask.session.clear()
	return "session cleared" 

@app.route('/error/<int:error_code>')
def show_error(error_code):
	return flask.render_template('{}.html'.format(error_code))

def __create_oauth_url(**kwargs):
	client_secret_file = '../client_secret.json'
	with open(client_secret_file, mode='r') as f:
		client_id = json.loads(f.read())['web']['client_id']
	values = {'response_type' : 'code',
			'client_id' : client_id,
			'redirect_uri' : REDIRECT_URL,
			'scope' : ' '.join(SCOPE),
			'access_type' : 'offline',
			'include_granted_scopes' : 'true'}
	values.update(kwargs)
	params = urllib.parse.urlencode(values)
	return BASE_URL % params
	

if __name__ == '__main__':
	pass

