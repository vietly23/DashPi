import flask
import urllib.parse
import json
import hashlib
import os

app = flask.Flask(__name__)
app.secret_key = '3512a68c-3b77-474f-b807-0a24d73ac98b'
app.debug = True

SCOPE = ['https://www.googleapis.com/auth/calendar.readonly',
			'https://www.googleapis.com/auth/gmail.readonly'
			]

#FLOW = client.flow_from_clientsecrets('../client_secret.json', SCOPE,
		#redirect_uri='http://www.192.168.0.196.xip.io:5000/oauth2callback')

#REDIRECT_URI='http://www.192.168.0.196.xip.io:5000/oauth2callback'

@app.route('/')
def index():
	if 'google_credentials' in flask.session:
		return 'Hello World!'
	else:
		return flask.redirect(flask.url_for('login'), 302)

@app.route('/login')
def login():
	state = hashlib.sha256(os.urandom(1024)).hexdigest()
	flask.session['state'] = state
	state_str = urllib.parse.urlencode({'state': state})
	auth_uri = G_LOGIN_URL + "&{}".format(state_str)
	return flask.render_template('login.html', auth_uri=auth_uri) 

@app.route('/oauth2callback')
def oauth2callback():
	if flask.request.args.get('error') == 'access_denied':
		return flask.redirect(flask.url_for('login'))
	if 'state' not in flask.session:
		return flask.redirect(flask.url_for('login'))
	elif flask.request.args.get('state') != flask.session['state']:
			return flask.redirect(flask.url_for('login'))
	else:
		auth_code = flask.request.args.get('code')
		credentials = FLOW.step2_exchange(auth_code)
		flask.session['google_credentials'] = credentials.to_json()
		return flask.redirect(flask.url_for('index'))

@app.route('/logout')
def logout():
	flask.session.clear()
	return "session cleared" 

def __create_oauth_url(**kwargs):
	client_secret_file = '../client_secret.json'
	with open(client_secret_file, mode='r') as f:
		client_id = json.loads(f.read())['web']['client_id']
	values = {'response_type' : 'code',
			'client_id' : client_id,
			'redirect_uri' : REDIRECT_URI,
			'scope' : ' '.join(SCOPE),
			'access_type' : 'offline',
			'include_granted_scopes' : 'true'}
	values.update(kwargs)
	params = urllib.parse.urlencode(values)
	return BASE_URL % params
	
REDIRECT_URI='http://localhost:5000/oauth2callback'
BASE_URL = 'https://accounts.google.com/o/oauth2/v2/auth?%s'
G_LOGIN_URL = __create_oauth_url() 

if __name__ == '__main__':
	pass

